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
import cairo

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class TransparentBackground:

    @classmethod
    def uuid(self) -> str:
        return 'empty'

    @classmethod
    def to_inner(cls, ctx, w, h):
        return w, h

    @classmethod
    def paint(cls, *_):
        pass

    @classmethod
    def stroke_frame_path(cls, ctx, w, h, border):
        return False

    @classmethod
    def max_textlen(cls):
        return 4

    @classmethod
    def adjust_dimensions(cls, w, h):
        return w, h

    @classmethod
    def background_color(cls, config):
        return None

class BackgroundImage:
    """ Helper class for creating the background of an OSMC symbol.
    """
    FRAME_WIDTH = 2.0

    def __init__(self, color: str, symbol: str | None) -> None:
        self.color = color
        self.symbol = symbol if symbol is None or hasattr(self, '_paint_' + symbol) else None

    def uuid(self) -> str:
        return f"{self.color}-{self.symbol}" if self.symbol else self.color

    def to_inner(self, ctx, w, h):
        """ Restricts the part to be used for drawing the foreground
            if necessary. Only used for framed backgrounds.
        """
        match self.symbol:
            case 'circle' | 'frame':
                ctx.translate(self.FRAME_WIDTH, self.FRAME_WIDTH)
                return w - 2 * self.FRAME_WIDTH, h - 2 * self.FRAME_WIDTH
            case 'diamond':
                ctx.translate(0.05 * w, 0.05 * h)
                return 0.9 * w, 0.9 * h
            case 'diamond_line':
                ctx.translate(0.05 * w + self.FRAME_WIDTH, 0.05 * h + self.FRAME_WIDTH)
                return 0.9 * w - self.FRAME_WIDTH * 2, 0.9 * h - self.FRAME_WIDTH * 2
            case _:
                return w, h

    def paint(self, ctx, w, h, config):
        """ Draw the background as described.
            Will adjust the canvas for drawing of the inner part.
        """
        if self.symbol is not None:
            ctx.set_source_rgb(*config.osmc_colors[self.color])
            func = getattr(self, f'_paint_{self.symbol}')
            func(ctx, w, h, config)


    def stroke_frame_path(self, ctx, w, h, border):
        match self.symbol:
            case 'circle' | 'round':
                return self._frame_path_circle(ctx, w, h, border)
            case 'diamond' | 'diamond_line':
                return self._frame_path_diamond(ctx, w, h, border)
            case _:
                False

    def max_textlen(self):
        match self.symbol:
            case 'stripe' | 'bar':
                return 0
            case 'diamond' | 'diamond_line':
                return 1
            case _:
                return TransparentBackground.max_textlen()

    def adjust_dimensions(self, w, h):
        match self.symbol:
            case 'stripe':
                return 0.6*w, h
            case 'bar':
                return w, 0.6*h
            case 'diamond' | 'diamond_line':
                return int(1.4 * w), h
            case _:
                return w, h

    def background_color(self, config):
        match self.symbol:
            case 'circle' | 'frame' | 'diamond_line':
                return config.osmc_colors['black' if self.color == 'white' else 'white']
            case _:
                return config.osmc_colors[self.color]

    def _paint_bar(self, *_):
        pass # only changes dimensions

    def _paint_stripe(self, *_):
        pass # only changes dimensions

    def _paint_diamond(self, ctx, w, h, config):
        pass

    def _paint_diamond_line(self, ctx, w, h, config):
        ctx.set_line_width(self.FRAME_WIDTH)
        ctx.move_to(0.5 * w, self.FRAME_WIDTH / 2)
        ctx.line_to(w - self.FRAME_WIDTH / 2, 0.5 * h)
        ctx.line_to(0.5 * w, h - self.FRAME_WIDTH / 2)
        ctx.line_to(self.FRAME_WIDTH / 2, 0.5 * h)
        ctx.close_path()
        ctx.stroke()


    def _paint_circle(self, ctx, w, h, config):
        ctx.save()
        ctx.scale(w, h)
        ctx.arc(0.5, 0.5, 0.5 - self.FRAME_WIDTH / min(w, h) / 2, 0, 2 * pi)
        ctx.restore()
        ctx.set_line_width(self.FRAME_WIDTH)
        ctx.stroke()

    def _paint_frame(self, ctx, w, h, config):
        ctx.set_line_width(self.FRAME_WIDTH)
        ctx.rectangle(self.FRAME_WIDTH/2, self.FRAME_WIDTH/2,
                      w - self.FRAME_WIDTH, h - self.FRAME_WIDTH)
        ctx.stroke()

    def _paint_round(self, ctx, w, h, config):
        pass

    def _frame_path_circle(self, ctx, w, h, border):
        ctx.save()
        ctx.scale(w, h) # needed, so we can draw an ellipse
        ctx.arc(0.5, 0.5, 0.5 - border / min(w, h), 0, 2 * pi)
        ctx.restore()
        return True

    def _frame_path_diamond(self, ctx, w, h, border):
        ctx.move_to(w/2, border)
        ctx.line_to(w - border, h/2)
        ctx.line_to(w/2, h - border)
        ctx.line_to(border, h/2)
        ctx.close_path()
        return True

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
        return f"{self.color}-{self.symbol}"

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
        ctx.move_to(0.15, 0.15)
        ctx.line_to(0.15, 0.85)
        ctx.line_to(0.85, 0.5)
        ctx.close_path()
        ctx.stroke()

    def _paint_right_pointer_line(self, ctx):
        self._paint_pointer_line(ctx)

    def _paint_left_pointer_line(self, ctx):
        ctx.set_line_width(0.15)
        ctx.move_to(0.85, 0.15)
        ctx.line_to(0.85, 0.85)
        ctx.line_to(0.15, 0.5)
        ctx.close_path()
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
        w, h = self.bg.adjust_dimensions(self.config.image_width or 16,
                                         self.config.image_height or 16)

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

    def render(self, ctx):
        w, h = self.render_background(ctx, self.bg.background_color(self.config))

        ctx.save()
        innerw, innerh = self.bg.to_inner(ctx, w, h)

        # foreground gets painted with 1,1 matrix
        if self.fgs:
            ctx.save()
            ctx.scale(innerw, innerh)
            for fg in self.fgs:
                fg.paint(ctx, self)
            ctx.restore()

        # reference text gets painted with original scale
        if self.ref:
            layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

            bnd_wd = self.config.text_border_width or 1.5

            self.render_layout(
                ctx, layout, color=self.config.osmc_colors[self.textcolor],
                x=(innerw - tw)/2,
                y=(innerh - bnd_wd - baseh)/2.0)

        ctx.restore() # restore to full image
        self.bg.paint(ctx, w, h, self.config)

    def render_frame(self, ctx):
        w, h = self.dimensions()
        border = self.config.image_border_width or 0

        # None-rectangular shapes require clipping. This is not yet supported
        # by Mapnik, so we'll resort to the rectangular frame here.
        if self.bg.stroke_frame_path(ctx, w, h, border):
            ctx.rectangle(0, 0, w, h)
            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.set_fill_rule(cairo.FillRule.EVEN_ODD)
            ctx.fill()

        ctx.rectangle(border/2, border/2, w - border, h - border)
        ctx.set_source_rgb(*self.config.border_color)
        ctx.set_line_width(border)
        ctx.stroke()

    def render_svg(self, ctx, name, color):
        content = self.find_resource(self.config.osmc_path, name + '.svg')
        content = re.sub('#000000',
                         '#{:02x}{:02x}{:02x}'.format(*[int(x*255) for x in self.config.osmc_colors[color]]),
                         content.decode('utf8')).encode()

        svg = Rsvg.Handle.new_from_data(content)

        ctx.save()
        ctx.translate(0.05, 0.05)
        ctx.scale(0.9/svg.props.width, 0.9/svg.props.height)
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
        if ref and len(ref) <= self.bg.max_textlen():
            self.ref = ref

            if color in self.config.osmc_colors:
                self.textcolor = color


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if config.osmc_colors is None:
        return None

    symbol = OsmcSymbol(tags.get('osmc:symbol'), config)

    return None if symbol.is_empty() else symbol
