# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import re
import os
from math import pi
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker


class OsmcSymbol(RefShieldMaker):
    """ Shield that follows the osmc:symbol specification.
    """

    def __init__(self, symbol, config):
        self.config = config
        self.ref = ''
        self.bgsymbol = None
        self.bgcolor = None
        self.fgsymbol = None
        self.fgcolor = None
        self.fgsecondary = None
        self.textcolor = 'black'

        part_handlers = (self._init_way_color,
                         self._init_bg_symbol,
                         self._init_fg_symbol,
                         self._init_ref,
                         self._init_text_color)

        for part, handler in zip(symbol.split(':', 4), part_handlers):
            handler(part.strip())

    def dimensions(self):
        w = self.config.image_width or 16
        h = self.config.image_height or 16

        if self.ref:
            tw, _ = self._get_text_size(self.config.text_font)
            text_border = self.config.text_border_width or 1.5
            image_border = self.config.image_border_width or 2.5
            w = max(w, int(tw + 2 * text_border + 2 * image_border))
            h += int(self.config.image_border_width or 0)

        return w, h

    def uuid(self):
        parts = ['osmc', self.config.style or 'None', self.bgcolor or 'empty']
        for part in (self.bgsymbol, self.fgsymbol, self.fgcolor, self.fgsecondary):
            if part is not None:
                parts.append(part)
        if self.ref:
            parts.append(self.ref_uuid())
            parts.append(self.textcolor)

        return '_'.join(parts)

    def render(self, ctx, w, h):
        ctx.save()
        ctx.scale(w, h)

        # background
        if self.bgcolor is not None:
            if self.bgsymbol is None:
                col = self.bgcolor
            else:
                col = 'black' if self.bgcolor == 'white' else 'white'
            self.render_background(ctx, 1, 1, self.config.osmc_colors[col])
        else:
            ctx.set_source_rgba(0,0,0,0) # transparent
            ctx.rectangle(0, 0, 1, 1)
            ctx.fill()

        if self.bgsymbol is not None:
            ctx.set_source_rgb(*self.config.osmc_colors[self.bgcolor])
            func = getattr(self, f'paint_bg_{self.bgsymbol}')
            func(ctx)
            # with a background image, make the foreground image a bit
            # smaller, so that it fits
            ctx.translate(0.2,0.2)
            ctx.scale(0.6,0.6)

        # secondary stripe fill
        if self.fgsecondary is not None:
            ctx.set_source_rgb(*self.config.osmc_colors[self.fgsecondary])
            ctx.set_line_width(0.3)
            self.paint_fg_right(ctx)

        # foreground fill
        if self.fgsymbol is not None:
            ctx.set_source_rgb(*self.config.osmc_colors[self.fgcolor])
            ctx.set_line_width(0.3)
            func = getattr(self, f'paint_fg_{self.fgsymbol}')
            func(ctx)

        ctx.restore()
        # reference text
        if self.ref:
            layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

            bnd_wd = self.config.text_border_width or 1.5

            self.render_layout(
                ctx, layout, color=self.config.osmc_colors[self.textcolor],
                x=(w - tw)/2,
                y=(h - bnd_wd - baseh)/2.0)

    def _init_way_color(self, color):
        pass # field is ignored at the moment

    def _init_bg_symbol(self, symbol):
        parts = symbol.split('_', 1)

        if parts[0] in self.config.osmc_colors:
            self.bgcolor = parts[0]

            if len(parts) > 1 and hasattr(self, 'paint_bg_' + parts[1]):
                self.bgsymbol = parts[1]

    def _init_fg_symbol(self, symbol):
        if symbol != "red_diamond" and hasattr(self, 'paint_fg_' + symbol):
            self.fgsymbol = symbol
            self.fgcolor = 'yellow' if symbol.startswith('shell') else 'black'
        else:
            parts = symbol.split('_', 1)
            if len(parts) > 1 and hasattr(self, 'paint_fg_' + parts[1]):
                self.fgsymbol = parts[1]
                self.fgcolor = parts[0] if parts[0] in self.config.osmc_colors else 'black'

    def _init_ref(self, ref):
        # XXX hack warning, limited support of second foreground on request
        # of Isreali mappers
        if self.fgcolor == 'blue' and self.fgsymbol == 'stripe' \
           and ref in ('orange_stripe_right', 'green_stripe_right'):
            self.fgsecondary = ref[:ref.index('_')]
        elif len(ref) <= 4:
            self.ref = ref

    def _init_text_color(self, color):
        if color in self.config.osmc_colors:
            self.textcolor = color

    def paint_bg_circle(self, ctx):
        ctx.set_line_width(0.1)
        ctx.arc(0.5, 0.5, 0.4, 0, 2*pi)
        ctx.stroke()

    def paint_bg_frame(self, ctx):
        ctx.set_line_width(0.1)
        ctx.rectangle(0.15, 0.15, 0.7, 0.7)
        ctx.stroke()

    def paint_bg_round(self, ctx):
        ctx.arc(0.5, 0.5, 0.4, 0, 2*pi)
        ctx.fill()

    def paint_fg_arch(self, ctx):
        ctx.set_line_width(0.22)
        ctx.move_to(0.25,0.9)
        ctx.arc(0.5,0.5,0.25, pi, 0)
        ctx.line_to(0.75,0.9)
        ctx.stroke()

    def paint_fg_backslash(self, ctx):
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.stroke()

    def paint_fg_bar(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(1, 0.5)
        ctx.stroke()

    def paint_fg_circle(self, ctx):
        ctx.set_line_width(0.21)
        ctx.arc(0.5, 0.5, 0.33, 0, 2*pi)
        ctx.stroke()

    def paint_fg_corner(self, ctx):
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.line_to(1, 0)
        ctx.close_path()
        ctx.fill()

    def paint_fg_cross(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(1, 0.5)
        ctx.stroke()
        ctx.move_to(0.5, 0)
        ctx.line_to(0.5, 1)
        ctx.stroke()

    def paint_fg_diamond_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.1, 0.5)
        ctx.line_to(0.5, 0.1)
        ctx.line_to(0.9, 0.5)
        ctx.line_to(0.5, 0.9)
        ctx.close_path()
        ctx.stroke()

    def paint_fg_diamond(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(0.5, 0.25)
        ctx.line_to(1, 0.5)
        ctx.line_to(0.5, 0.75)
        ctx.fill()

    def paint_fg_dot(self, ctx):
        ctx.arc(0.5, 0.5, 0.29, 0, 2*pi)
        ctx.fill()

    def paint_fg_fork(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(1, 0.5)
        ctx.line_to(0.45, 0.5)
        ctx.line_to(0, 0.1)
        ctx.stroke()
        ctx.move_to(0.45, 0.5)
        ctx.line_to(0, 0.9)
        ctx.stroke()

    def paint_fg_lower(self, ctx):
        ctx.rectangle(0, 0.5, 1, 0.5)
        ctx.fill()

    def paint_fg_right(self, ctx):
        ctx.rectangle(0.5, 0, 0.5, 1)
        ctx.fill()

    def paint_fg_pointer(self, ctx):
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.5)
        ctx.fill()

    def paint_fg_rectangle_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.rectangle(0.25, 0.25, 0.5, 0.5)
        ctx.stroke()

    def paint_fg_rectangle(self, ctx):
        ctx.rectangle(0.25, 0.25, 0.5, 0.5)
        ctx.fill()

    def paint_fg_red_diamond(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(0.5, 0.25)
        ctx.line_to(0.5, 0.75)
        ctx.fill()
        ctx.set_source_rgb(*self.config.osmc_colors['red'])
        ctx.move_to(0.5, 0.25)
        ctx.line_to(1, 0.5)
        ctx.line_to(0.5, 0.75)
        ctx.fill()

    def paint_fg_slash(self, ctx):
        ctx.move_to(1, 0)
        ctx.line_to(0, 1)
        ctx.stroke()

    def paint_fg_stripe(self, ctx):
        ctx.move_to(0.5, 0)
        ctx.line_to(0.5, 1)
        ctx.stroke()

    def paint_fg_triangle_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.2, 0.8)
        ctx.line_to(0.5, 0.2)
        ctx.line_to(0.8, 0.8)
        ctx.close_path()
        ctx.stroke()

    def paint_fg_triangle(self, ctx):
        ctx.move_to(0.2, 0.8)
        ctx.line_to(0.5, 0.2)
        ctx.line_to(0.8, 0.8)
        ctx.fill()

    def paint_fg_triangle_turned(self, ctx):
        ctx.move_to(0.2, 0.2)
        ctx.line_to(0.5, 0.8)
        ctx.line_to(0.8, 0.2)
        ctx.fill()

    def paint_fg_turned_T(self, ctx):
        ctx.set_line_width(0.2)
        ctx.move_to(0.1, 0.8)
        ctx.line_to(0.9, 0.8)
        ctx.move_to(0.5, 0.2)
        ctx.line_to(0.5, 0.8)
        ctx.stroke()

    def paint_fg_x(self, ctx):
        ctx.set_line_width(0.25)
        ctx.move_to(1, 0)
        ctx.line_to(0, 1)
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.stroke()

    def paint_fg_hexagon(self, ctx):
        ctx.move_to(0.8, 0.5)
        ctx.line_to(0.65, 0.24)
        ctx.line_to(0.35, 0.24)
        ctx.line_to(0.2, 0.5)
        ctx.line_to(0.35, 0.76)
        ctx.line_to(0.65, 0.76)
        ctx.fill()

    def paint_fg_shell(self, ctx):
        al = ctx.get_antialias()
        #ctx.set_antialias(cairo.ANTIALIAS_NONE)
        if self.fgcolor is None:
            ctx.set_source_rgb(*self.config.osmc_colors['black'])
        ctx.set_line_width(0.06)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0,0.3)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.1,0.5)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.2,0.65)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.35,0.8)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.5,0.85)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.65,0.8)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.8,0.65)
        ctx.move_to(0.5,0.1)
        ctx.line_to(0.9,0.5)
        ctx.move_to(0.5,0.1)
        ctx.line_to(1,0.3)
        ctx.stroke()
        ctx.set_antialias(al)

    def paint_fg_shell_modern(self, ctx):
        al = ctx.get_antialias()
        #ctx.set_antialias(cairo.ANTIALIAS_NONE)
        if self.fgcolor is None:
            ctx.set_source_rgb(*self.config.osmc_colors['yellow'])
        ctx.set_line_width(0.06)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.3,0)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.5,0.1)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.65,0.2)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.8,0.35)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.85,0.5)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.8,0.65)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.65,0.8)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.5,0.9)
        ctx.move_to(0.1,0.5)
        ctx.line_to(0.3,1)
        ctx.stroke()
        ctx.set_antialias(al)

    def paint_fg_hiker(self, ctx):
        self._src_from_svg(ctx, 'hiker.svg')

    def paint_fg_wheel(self, ctx):
        ctx.save()
        self._src_from_svg(ctx, 'wheel.svg')

    def _src_from_svg(self, ctx, name):
        content = self.find_resource(self.config.osmc_path, name)
        if self.fgcolor is not None:
            fgcol = tuple([int(x*255) for x in self.config.osmc_colors[self.fgcolor]])
            color = '#%02x%02x%02x' % fgcol
            content = re.sub('#000000', color, content.decode('utf8')).encode()

        svg = Rsvg.Handle.new_from_data(content)

        w, h = self.dimensions()
        b = self.config.image_border_width or 0
        bw, bh = b/w, b/h

        ctx.save()
        ctx.translate(bw, bh)
        ctx.scale((1.0 - 2.0*bw)/svg.props.width, (1.0 - 2.0*bh)/svg.props.height)
        svg.render_cairo(ctx)
        ctx.restore()


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if config.osmc_colors is None:
        return None

    symbol = tags.get('osmc:symbol')
    if symbol is None or ':' not in symbol:
        return None

    return OsmcSymbol(symbol, config)
