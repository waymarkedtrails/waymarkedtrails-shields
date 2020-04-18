# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann
#
# This is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
from io import BytesIO
from xml.dom.minidom import parseString as xml_parse
from xml.parsers.expat import ExpatError

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Pango, PangoCairo, Rsvg


class ShieldMaker(object):
    """ Base class for all shield making objects. It implements some common
        functionality.
    """

    def dimensions(self):
        return (self.config.image_width or 16, self.config.image_height or 16)

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
            buf = self._mangle_svg(buf.decode('UTF8')).encode('UTF8')

        return buf


    def _render_border(self, ctx, w, h):
        """ Create a border around the image if that was configured.
        """
        border_width = self.config.image_border_width or 0
        if border_width <= 0:
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
            use_ele = svg.getElementsByTagName("use")

            if sym_ele.length == 0 or use_ele.length == 0:
                continue

            symbols = {}
            for e in sym_ele:
                symbols['#' + e.getAttribute('id')] = e.cloneNode(True)
                e.parentNode.removeChild(e)

            for e in use_ele:
                ref = e.getAttribute('xlink:href')
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

        return dom.toxml()


class RefShieldMaker(ShieldMaker):
    """ A shield maker for shields where the width depends on the text
        size.
    """

    def uuid(self):
        """ Compute the uuid from a `self.prefix` and the properly
            encoded `self.ref`.
        """
        return self.uuid_prefix + ''.join(["%04x" % ord(x) for x in self.ref])

    def _get_text_size(self):
        """ Compute the rendered size of `self.ref` in pixels.
        """
        txtctx_layout = PangoCairo.create_layout(
                           cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 10,10)))
        fnt = self.config.text_font
        if fnt is not None:
            txtctx_layout.set_font_description(Pango.FontDescription(fnt))
        txtctx_layout.set_text(self.ref, -1)

        return txtctx_layout.get_pixel_size()
