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

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Pango, PangoCairo, Rsvg

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class RefColorSymbol(RefShieldMaker):
    """ A shield with a reference with a colored underline according to the
        color tag.
    """

    def __init__(self, ref, name, color, config):
        self.config = config
        self.ref = ref
        self.color = color
        self.uuid_prefix = "ctb_{}_{}_".format(self.config.style or '', name)

    def dimensions(self):
        tw, _ = self._get_text_size()
        text_border = self.config.text_border_width or 1.5
        image_border = self.config.image_border_width or 2.5
        w = int(tw + 2 * text_border + 2 * image_border)
        h = int((self.config.image_height or 16) + image_border)
        return (w, h)


    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, (1., 1., 1.))

        image_border = self.config.image_border_width or 2.5

        # bar with halo
        ctx.set_line_width(0)
        ctx.set_source_rgb(*self.color[1])
        ctx.rectangle(image_border + 1.8, h - 3.2 - image_border,
                      w - 2 * (image_border + 1.8) , 3.4)
        ctx.fill()
        ctx.set_source_rgb(*self.color[0])
        ctx.rectangle(image_border + 2, h - 3 - image_border,
                      w - 2 * (image_border + 2) , 3)
        ctx.fill()

        ## reference text
        txtcol = self.config.text_color or (0, 0, 0)
        ctx.set_source_rgb(*txtcol)
        layout = PangoCairo.create_layout(ctx)
        fnt = self.config.text_font
        if fnt is not None:
            layout.set_font_description(Pango.FontDescription(fnt))
        layout.set_text(self.ref, -1)
        tw, th = layout.get_pixel_size()
        bnd_wd = self.config.text_border_width or 1.5
        PangoCairo.update_layout(ctx, layout)
        ctx.move_to((w - tw)/2,
                    (h - bnd_wd - layout.get_iter().get_baseline()/Pango.SCALE)/2.0)
        PangoCairo.show_layout(ctx, layout)


    def _get_text_size(self):
        """ Comute the rendered size of the ref in pixels.
        """
        txtctx_layout = PangoCairo.create_layout(
                           cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 10,10)))
        fnt = self.config.text_font
        if fnt is not None:
            txtctx_layout.set_font_description(Pango.FontDescription(fnt))
        txtctx_layout.set_text(self.ref, -1)

        return txtctx_layout.get_pixel_size()



def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.make_ref(names=('name', 'osmc:name'))
    if ref is None:
        return None

    color = tags.as_color(('color', 'colour'), config.colorbox_names or {})
    if color is None:
        return None

    if color[0].startswith('#'):
        return RefColorSymbol(ref, color[0], (color[1], (1., 1., 1.)), config)

    return RefColorSymbol(ref, *color, config)
