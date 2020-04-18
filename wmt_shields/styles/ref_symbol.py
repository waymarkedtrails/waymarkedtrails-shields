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

def _encode_ref(ref):
    return ''.join(["%04x" % ord(x) for x in ref])

class RefSymbol(RefShieldMaker):

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref
        if self.config.style:
            self.uuid_prefix = "ref_{}_".format(self.config.style)
        else:
            self.uuid_prefix = "ref_"

    def dimensions(self):
        tw, _ = self._get_text_size()
        text_border = self.config.text_border_width or 1.5
        image_border = self.config.image_border_width or 2.5
        w = int(tw + 2 * text_border + 2 * image_border)

        return (w, self.config.image_height or 16)

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, self.config.text_bgcolor)

        # reference text
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


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.make_ref(names=('name', 'osmc:name'))
    if ref is None:
        return None

    return RefSymbol(ref, config)
