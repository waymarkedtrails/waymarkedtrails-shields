# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import sys
import pkg_resources
import os
from io import BytesIO
from xml.dom.minidom import parseString as xml_parse
from xml.parsers.expat import ExpatError
from urllib.parse import urlparse
from urllib.request import urlopen

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

def load_shield_maker(spec):
    """ Return a shield maker object. An object may either be a class with
        a static `create_for` function or a string with a module containing a
        `create_for` function. If the string starts with a dot, then it is
        assumed to be one of the internal styles in the `wmt_shields.styles`
        directory.
    """
    if isinstance(spec, str):
        if spec.startswith('.'):
            spec = 'wmt_shields.styles' + spec
        try:
            __import__(spec)
            return sys.modules[spec]
        except ImportError:
            print("Style '{}' not found.".format(spec))
            raise

    return spec


class ShieldMaker(object):
    """ Base class for all shield making objects. It implements some common
        functionality.
    """

    def uuid(self):
        """ Return a unique identifier also usable as a filename. the default
            implementation expects a field `uuid_pattern` which needs to have
            one `{}` placeholder for the style name. If that is not sufficient
            then implementations may also just overwrite this function.
        """
        return self.uuid_pattern.format(self.config.style or 'None')

    def dimensions(self):
        """ Return a tuple of width and height of the final image (including
            borders). The default implementation returns `image_width` and
            `image_height` from the configurations. Implementations may
            override the function for custom sizes.
        """
        return (self.config.image_width or 16, self.config.image_height or 16)

    def find_resource(self, subdir, filename):
        subdir_str = str(subdir) if subdir is not None else ''
        filename = str(filename)
        if(urlparse(filename).netloc):
            with urlopen(filename) as response:
                return response.read()

        elif os.path.isabs(filename):
            abspath = filename
        elif subdir is not None \
           and (os.path.isabs(subdir_str) or subdir_str.startswith('{data}')):
            abspath = os.path.join(subdir_str, filename)
        else:
            abspath = os.path.join(self.config.data_dir or '', subdir_str,
                                   filename)

        if abspath.startswith('{data}'):
            return pkg_resources.resource_string('wmt_shields',
                                                 os.path.join('data',
                                                              abspath[7:]))

        with open(abspath, 'r') as f:
            content = f.read()

        return content.encode()

    def to_file(self, filename, format='svg'):
        """ Render the shield into the file `filename` using the output format
            `format`.
        """
        buf = self.create_image(format)

        with open(filename, 'wb') as of:
            of.write(buf)

    def create_image(self, format='svg'):
        """ Render the shield into a byte buffer using the output format
            `format`.
        """
        image = BytesIO()
        w, h = self.dimensions()

        if format == 'svg':
            surface = cairo.SVGSurface(image, w, h)
            major, minor, patch = cairo.version_info
            if major == 1 and minor >= 18:
                surface.set_document_unit(cairo.SVGUnit.PX)
        else:
            raise RuntimeError("Format {} not implemented.".format(format))

        ctx = cairo.Context(surface)
        ctx.save()
        self.render(ctx, w, h)
        ctx.restore()
        self._render_border(ctx, w, h)
        ctx.show_page()
        surface.finish()
        buf = image.getvalue()

        if format == 'svg':
            try:
                buf = self._mangle_svg(buf.decode('UTF8')).encode('UTF8')
            except Exception as ex:
                print(f"WARNING: cannot mangle image {self.uuid()}: {ex}")

        return buf


    def _render_border(self, ctx, w, h):
        """ Create a border around the image if that was configured.
        """
        border_width = self.config.image_border_width or 0
        color = self.config.border_color
        if border_width <= 0 or color is None:
            return

        ctx.rectangle(0, 0, w, h)
        ctx.set_line_width(self.config.image_border_width)
        ctx.set_source_rgb(*self.config.border_color)
        ctx.stroke()

    def render_background(self, ctx, w, h, color):
        if color is None:
            return

        ctx.rectangle(0, 0, w, h)
        ctx.set_source_rgb(*color)
        ctx.fill()

    def _mangle_svg(self, buf):
        try:
            dom = xml_parse(buf)
        except ExpatError:
            raise RuntimeError("Cannot parse SVG shield.")

        for svg in dom.getElementsByTagName("svg"):
            sym_ele = svg.getElementsByTagName("symbol")
            image_ele = svg.getElementsByTagName("image")
            use_ele = svg.getElementsByTagName("use")

            if sym_ele.length == 0 or use_ele.length == 0:
                continue

            symbols = {}
            for e in sym_ele:
                symbols['#' + e.getAttribute('id')] = e.cloneNode(True)
                e.parentNode.removeChild(e)

            # image elements are not supported by Mapnik. Remove.
            for e in image_ele:
                e.parentNode.removeChild(e)

            for e in use_ele:
                ref = e.getAttribute('xlink:href')

                if ref in symbols and e.hasAttribute('x') and e.hasAttribute('y'):
                    x   = float(e.getAttribute('x'))
                    y   = float(e.getAttribute('y'))

                    group = dom.createElement('g')

                    for ce in symbols[ref].childNodes:
                        node = ce.cloneNode(True)

                        if node.nodeName == 'path':
                            path = node.getAttribute('d')

                            newpath = ''
                            is_x = True
                            for p in path.split():
                                if not p:
                                    continue

                                if p[0].isupper():
                                    dx = x
                                    dy = y
                                    newpath += p + ' '
                                elif p[0].islower():
                                    dx = 0
                                    dy = 0
                                    newpath += p + ' '
                                elif p[0].isnumeric:
                                    val = float(p) + (dx if is_x else dy)
                                    is_x = not is_x
                                    newpath += "%f " % val

                            node.setAttribute('d', newpath)

                        group.appendChild(node)

                    e.parentNode.replaceChild(group, e)
                else:
                    e.parentNode.removeChild(e)

        return dom.toxml()


class RefShieldMaker(ShieldMaker):
    """ A shield maker for shields where the width depends on the text
        size.
    """

    def ref_uuid(self):
        return ''.join(["%04x" % ord(x) for x in self.ref])

    def _get_text_size(self, fnt):
        """ Compute the rendered size of `self.ref` in pixels.
        """
        l, _, _ = self.layout_ref(
                cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 10,10)), fnt)
        return l.get_pixel_size()

    def layout_ref(self, ctx, fnt):
        layout = PangoCairo.create_layout(ctx)
        if fnt is not None:
            layout.set_font_description(Pango.FontDescription(fnt))
        layout.set_text(self.ref, -1)
        tw, _ = layout.get_pixel_size()
        baseh = layout.get_iter().get_baseline()/Pango.SCALE

        return layout, tw, baseh

    def render_layout(self, ctx, layout, color, x, y):
        if color is None:
            ctx.set_source_rgb(1., 1., 1.) # black
        else:
            ctx.set_source_rgb(*color)

        PangoCairo.update_layout(ctx, layout)
        ctx.move_to(x, y)
        PangoCairo.show_layout(ctx, layout)
