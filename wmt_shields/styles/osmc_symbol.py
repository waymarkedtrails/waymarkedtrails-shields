# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2025 Sarah Hoffmann

import re
import os
from math import pi
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class TransparentBackground:

    @classmethod
    def uuid(self) -> str:
        return 'empty'

    @classmethod
    def paint(cls, ctx, _):
        ctx.set_source_rgba(0, 0, 0, 0) # transparent
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()

class BackgroundImage:
    """ Helper class for creating the background of an OSMC symbol.
    """

    def __init__(self, color: str, symbol: str | None) -> None:
        self.color = color
        self.symbol = symbol if symbol is None or hasattr(self, '_paint_' + symbol) else None

    def uuid(self) -> str:
        return f"{self.color}_{self.symbol}" if self.symbol else self.color

    def paint(self, ctx, config):
        """ Draw the background as described.
            Will adjust the canvas for drawing of the inner part.
        """
        if self.symbol is None:
            col = self.color
        else:
            col = 'black' if self.color == 'white' else 'white'

        ctx.rectangle(0, 0, 1, 1)
        ctx.set_source_rgb(*config.osmc_colors[col])
        ctx.fill()

        if self.symbol is not None:
            ctx.set_source_rgb(*config.osmc_colors[self.color])
            func = getattr(self, f'_paint_{self.symbol}')
            func(ctx)
            # with a background image, make the foreground image a bit
            # smaller, so that it fits
            ctx.translate(0.2,0.2)
            ctx.scale(0.6,0.6)

    def _paint_circle(self, ctx):
        ctx.set_line_width(0.1)
        ctx.arc(0.5, 0.5, 0.4, 0, 2*pi)
        ctx.stroke()

    def _paint_frame(self, ctx):
        ctx.set_line_width(0.1)
        ctx.rectangle(0.15, 0.15, 0.7, 0.7)
        ctx.stroke()

    def _paint_round(self, ctx):
        ctx.arc(0.5, 0.5, 0.4, 0, 2*pi)
        ctx.fill()


class ForegroundImage:
    """ Helper class for adding a foreground to an OSMC symbol.
    """

    def __init__(self, color: str | None, symbol: str) -> None:
        if color is None:
            self. color = 'yellow' if symbol.startswith('shell') else 'black'
        else:
            self.color = color
        self.symbol = symbol

    @classmethod
    def has_symbol(self, symbol: str) -> bool:
        return hasattr(self, '_paint_' + symbol)

    def uuid(self) -> str:
        return f"{self.symbol}_{self.color}"

    def paint(self, ctx, shield):
        self._config = shield.config
        ctx.set_source_rgb(*self._config.osmc_colors[self.color])
        ctx.set_line_width(0.3)
        getattr(self, f'_paint_{self.symbol}')(ctx)

    def _paint_arch(self, ctx):
        ctx.set_line_width(0.22)
        ctx.move_to(0.25,0.9)
        ctx.arc(0.5,0.5,0.25, pi, 0)
        ctx.line_to(0.75,0.9)
        ctx.stroke()

    def _paint_backslash(self, ctx):
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.stroke()

    def _paint_bar(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(1, 0.5)
        ctx.stroke()

    def _paint_circle(self, ctx):
        ctx.set_line_width(0.21)
        ctx.arc(0.5, 0.5, 0.33, 0, 2*pi)
        ctx.stroke()

    def _paint_corner(self, ctx):
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.line_to(1, 0)
        ctx.close_path()
        ctx.fill()

    def _paint_corner_left(self, ctx):
        ctx.move_to(1, 0)
        ctx.line_to(0, 1)
        ctx.line_to(0, 0)
        ctx.close_path()
        ctx.fill()

    def _paint_cross(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(1, 0.5)
        ctx.stroke()
        ctx.move_to(0.5, 0)
        ctx.line_to(0.5, 1)
        ctx.stroke()

    def _paint_diamond_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.1, 0.5)
        ctx.line_to(0.5, 0.1)
        ctx.line_to(0.9, 0.5)
        ctx.line_to(0.5, 0.9)
        ctx.close_path()
        ctx.stroke()

    def _paint_diamond(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(0.5, 0.25)
        ctx.line_to(1, 0.5)
        ctx.line_to(0.5, 0.75)
        ctx.fill()

    def _paint_diamond_left(self, ctx):
        ctx.move_to(0, 0.5)
        ctx.line_to(0.5, 0.25)
        ctx.line_to(0.5, 0.75)
        ctx.fill()

    def _paint_diamond_right(self, ctx):
        ctx.line_to(0.5, 0.25)
        ctx.line_to(1, 0.5)
        ctx.line_to(0.5, 0.75)
        ctx.fill()

    def _paint_dot(self, ctx):
        ctx.arc(0.5, 0.5, 0.29, 0, 2*pi)
        ctx.fill()

    def _paint_fork(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(1, 0.5)
        ctx.line_to(0.45, 0.5)
        ctx.line_to(0, 0.1)
        ctx.stroke()
        ctx.move_to(0.45, 0.5)
        ctx.line_to(0, 0.9)
        ctx.stroke()

    def _paint_lower(self, ctx):
        ctx.rectangle(0, 0.5, 1, 0.5)
        ctx.fill()

    def _paint_upper(self, ctx):
        ctx.rectangle(0, 0, 1, 0.5)
        ctx.fill()

    def _paint_right(self, ctx):
        ctx.rectangle(0.5, 0, 0.5, 1)
        ctx.fill()

    def _paint_left(self, ctx):
        ctx.rectangle(0, 0, 0.5, 1)
        ctx.fill()

    def _paint_pointer(self, ctx):
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.5)
        ctx.fill()

    def _paint_right_pointer(self, ctx):
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.5)
        ctx.fill()

    def _paint_left_pointer(self, ctx):
        ctx.move_to(0.9, 0.1)
        ctx.line_to(0.9, 0.9)
        ctx.line_to(0.1, 0.5)
        ctx.fill()

    def _paint_pointer_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.5)
        ctx.line_to(0.1, 0.1)
        ctx.stroke()

    def _paint_right_pointer_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.5)
        ctx.line_to(0.1, 0.1)
        ctx.stroke()

    def _paint_left_pointer_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.9, 0.1)
        ctx.line_to(0.9, 0.9)
        ctx.line_to(0.1, 0.5)
        ctx.line_to(0.9, 0.1)
        ctx.stroke()

    def _paint_rectangle_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.rectangle(0.25, 0.25, 0.5, 0.5)
        ctx.stroke()

    def _paint_rectangle(self, ctx):
        ctx.rectangle(0.25, 0.25, 0.5, 0.5)
        ctx.fill()

    def _paint_slash(self, ctx):
        ctx.move_to(1, 0)
        ctx.line_to(0, 1)
        ctx.stroke()

    def _paint_stripe(self, ctx):
        ctx.move_to(0.5, 0)
        ctx.line_to(0.5, 1)
        ctx.stroke()

    def _paint_triangle_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.2, 0.8)
        ctx.line_to(0.5, 0.2)
        ctx.line_to(0.8, 0.8)
        ctx.close_path()
        ctx.stroke()

    def _paint_triangle(self, ctx):
        ctx.move_to(0.2, 0.8)
        ctx.line_to(0.5, 0.2)
        ctx.line_to(0.8, 0.8)
        ctx.fill()

    def _paint_triangle_turned(self, ctx):
        ctx.move_to(0.2, 0.2)
        ctx.line_to(0.5, 0.8)
        ctx.line_to(0.8, 0.2)
        ctx.fill()

    def _paint_turned_T(self, ctx):
        ctx.set_line_width(0.2)
        ctx.move_to(0.1, 0.8)
        ctx.line_to(0.9, 0.8)
        ctx.move_to(0.5, 0.2)
        ctx.line_to(0.5, 0.8)
        ctx.stroke()

    def _paint_x(self, ctx):
        ctx.set_line_width(0.25)
        ctx.move_to(1, 0)
        ctx.line_to(0, 1)
        ctx.move_to(0, 0)
        ctx.line_to(1, 1)
        ctx.stroke()

    def _paint_hexagon(self, ctx):
        ctx.move_to(0.8, 0.5)
        ctx.line_to(0.65, 0.24)
        ctx.line_to(0.35, 0.24)
        ctx.line_to(0.2, 0.5)
        ctx.line_to(0.35, 0.76)
        ctx.line_to(0.65, 0.76)
        ctx.fill()

    def _paint_shell(self, ctx):
        al = ctx.get_antialias()
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

    def _paint_shell_modern(self, ctx):
        al = ctx.get_antialias()
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

    def _paint_crest(self, ctx):
        ctx.move_to(0.15,0.5)
        ctx.line_to(0.15,0.05)
        ctx.line_to(0.85,0.05)
        ctx.line_to(0.85,0.5)
        ctx.curve_to(0.85,0.728,0.701,0.921,0.50,0.95)
        ctx.curve_to(0.299,0.921,0.148,0.728,0.15,0.50)
        ctx.fill()

    def _paint_arrow(self, ctx):
        ctx.move_to(0.1,0.7)
        ctx.line_to(0.55,0.7)
        ctx.line_to(0.55, 0.95)
        ctx.line_to(0.95, 0.5)
        ctx.line_to(0.55, 0.05)
        ctx.line_to(0.55, 0.3)
        ctx.line_to(0.1, 0.3)
        ctx.line_to(0.1, 0.7)
        ctx.fill()

    def _paint_right_arrow(self, ctx):
        ctx.move_to(0.1,0.7)
        ctx.line_to(0.55,0.7)
        ctx.line_to(0.55, 0.95)
        ctx.line_to(0.95, 0.5)
        ctx.line_to(0.55, 0.05)
        ctx.line_to(0.55, 0.3)
        ctx.line_to(0.1, 0.3)
        ctx.line_to(0.1, 0.7)
        ctx.fill()

    def _paint_left_arrow(self, ctx):
        ctx.move_to(0.9,0.7)
        ctx.line_to(0.45,0.7)
        ctx.line_to(0.45, 0.95)
        ctx.line_to(0.05, 0.5)
        ctx.line_to(0.45, 0.05)
        ctx.line_to(0.45, 0.3)
        ctx.line_to(0.9, 0.3)
        ctx.line_to(0.9, 0.7)
        ctx.fill()

    def _paint_up_arrow(self, ctx):
        ctx.move_to(0.7,0.9)
        ctx.line_to(0.7,0.45)
        ctx.line_to(0.95, 0.45)
        ctx.line_to(0.5, 0.05)
        ctx.line_to(0.05, 0.45)
        ctx.line_to(0.3, 0.45)
        ctx.line_to(0.3, 0.9)
        ctx.line_to(0.7, 0.9)
        ctx.fill()

    def _paint_down_arrow(self, ctx):
        ctx.move_to(0.7,0.1)
        ctx.line_to(0.7,0.55)
        ctx.line_to(0.95, 0.55)
        ctx.line_to(0.5, 0.95)
        ctx.line_to(0.05, 0.55)
        ctx.line_to(0.3, 0.55)
        ctx.line_to(0.3, 0.1)
        ctx.line_to(0.7, 0.1)
        ctx.fill()

    def _paint_bowl(self, ctx):
        ctx.move_to(0.05,0.5)
        ctx.line_to(0.95,0.5)
        ctx.arc(0.5,0.5,0.45,0,pi)
        ctx.fill()

    def _paint_upper_bowl(self, ctx):
        ctx.move_to(0.05,0.5)
        ctx.line_to(0.95,0.5)
        ctx.arc_negative(0.5,0.5,0.45,0,pi)
        ctx.fill()

    def _paint_house(self, ctx):
        ctx.move_to(0.2,0.9)
        ctx.line_to(0.2,0.4)
        ctx.line_to(0.5,0.1)
        ctx.line_to(0.8,0.4)
        ctx.line_to(0.8,0.9)
        ctx.line_to(0.2,0.9)
        ctx.fill()

    def _paint_L(self, ctx):
        ctx.set_line_width(0.3)
        ctx.move_to(0.2,0.05)
        ctx.line_to(0.2,0.8)
        ctx.line_to(0.95,0.8)
        ctx.stroke()

    def _paint_drop(self, ctx):
        ctx.move_to(0.5,0.2)
        ctx.line_to(0.9,0.5)
        ctx.line_to(0.5,0.8)
        ctx.arc(0.4,0.5,0.3,0.98,-0.98)
        ctx.fill()

    def _paint_drop_line(self, ctx):
        ctx.set_line_width(0.1)
        ctx.move_to(0.5,0.21)
        ctx.line_to(0.9,0.5)
        ctx.line_to(0.5,0.79)
        ctx.arc(0.4,0.5,0.3,0.98,-0.98)
        ctx.stroke()

class SvgImage:
    """ Helper class to render foregrounds from SVG.
    """
    AVAILABLE_SVGS = ('hiker', 'wheel')

    def __init__(self, color: str | None, symbol: str) -> None:
        self.color = color or 'black'
        self.symbol = symbol

    @classmethod
    def has_symbol(self, symbol: str) -> bool:
        return symbol in self.AVAILABLE_SVGS

    def uuid(self) -> str:
        return f"{self.symbol}_{self.color}"

    def paint(self, ctx, shield):
        shield.render_svg(ctx, self.symbol, self.color)


class OsmcSymbol(RefShieldMaker):
    """ Shield that follows the osmc:symbol specification.
    """

    def __init__(self, symbol, config):
        self.config = config
        self.ref = ''
        self.bg: BackgroundImage | TransparentBackground = TransparentBackground
        self.fgs: list[ForegourndImage] = []
        self.textcolor = 'black'

        if symbol is not None:
            parts = symbol.split(':', 5)
            num_parts = len(parts)

            self._init_way_color(parts[0].strip())
            if num_parts > 1:
                self._init_bg_symbol(parts[1].strip())
            if num_parts > 2:
                self._add_fg_symbol(parts[2].strip())
            match num_parts:
                case 4:
                    if not self._add_fg_symbol(parts[3].strip()):
                        self._init_ref(parts[3].strip(), 'black')
                case 5:
                    self._init_ref(parts[3].strip(), parts[4].strip())
                case 6:
                    self._add_fg_symbol(parts[3].strip())
                    self._init_ref(parts[4].strip(), parts[5].strip())

    def is_empty(self) -> bool:
        return not self.ref and not self.fgs and self.bg == TransparentBackground

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
        parts = ['osmc', self.config.style or 'None', self.bg.uuid()]
        parts.extend(fg.uuid() for fg in self.fgs)
        if self.ref:
            parts.append(self.ref_uuid())
            parts.append(self.textcolor)

        return '_'.join(parts)

    def render(self, ctx, w, h):
        ctx.save()
        ctx.scale(w, h)

        self.bg.paint(ctx, self.config)
        for fg in self.fgs:
            fg.paint(ctx, self)

        ctx.restore()
        # reference text
        if self.ref:
            layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

            bnd_wd = self.config.text_border_width or 1.5

            self.render_layout(
                ctx, layout, color=self.config.osmc_colors[self.textcolor],
                x=(w - tw)/2,
                y=(h - bnd_wd - baseh)/2.0)

    def render_svg(self, ctx, name, color):
        content = self.find_resource(self.config.osmc_path, name + '.svg')
        content = re.sub('#000000',
                         '#{:02x}{:02x}{:02x}'.format(*[int(x*255) for x in self.config.osmc_colors[color]]),
                         content.decode('utf8')).encode()

        svg = Rsvg.Handle.new_from_data(content)

        w, h = self.dimensions()
        b = self.config.image_border_width or 0
        bw, bh = b/w, b/h

        ctx.save()
        ctx.translate(bw, bh)
        ctx.scale((1.0 - 2.0*bw)/svg.props.width, (1.0 - 2.0*bh)/svg.props.height)
        svg.render_cairo(ctx)
        ctx.restore()

    def _init_way_color(self, color):
        pass # field is ignored at the moment

    def _init_bg_symbol(self, symbol):
        parts = symbol.split('_', 1)

        if parts[0] in self.config.osmc_colors:
            self.bg = BackgroundImage(parts[0],
                                      parts[1] if len(parts) > 1 else None)

    def _add_fg_symbol(self, symbol) -> bool:
        if SvgImage.has_symbol(symbol):
            self.fgs.append(SvgImage(None, symbol))
            return True

        if ForegroundImage.has_symbol(symbol):
            self.fgs.append(ForegroundImage(None, symbol))
            return True

        parts = symbol.split('_', 1)
        if len(parts) > 1:
            color = parts[0] if parts[0] in self.config.osmc_colors else 'black'
            if parts[1] == 'red_diamond':
                self.fgs.append(ForegroundImage(color, 'diamond'))
                self.fgs.append(ForegroundImage('red', 'diamond_right'))
                return True
            if ForegroundImage.has_symbol(parts[1]):
                self.fgs.append(ForegroundImage(color, parts[1]))
                return True
            if SvgImage.has_symbol(parts[1]):
                self.fgs.append(SvgImage(color, parts[1]))
                return True

        return False

    def _init_ref(self, ref, color):
        if ref and len(ref) <= 4:
            self.ref = ref

            if color in self.config.osmc_colors:
                self.textcolor = color


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if config.osmc_colors is None:
        return None

    symbol = OsmcSymbol(tags.get('osmc:symbol'), config)

    return None if symbol.is_empty() else symbol
