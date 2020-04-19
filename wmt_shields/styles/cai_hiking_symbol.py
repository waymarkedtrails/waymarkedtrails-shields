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

import re

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class CaiHikingSymbol(RefShieldMaker):
    """ A shield with nothing but a background color.
    """

    def __init__(self, typ, ref, config):
        self.config = config
        self.typ = typ
        self.ref = ref
        self.uuid_pattern = f"cai_{{}}_{typ}_{self.ref_uuid()}"

    def dimensions(self):
        tw, _ = self._get_text_size(self.config.text_font)

        # create an image where the text fits
        w = int(tw + 2 * self.config.cai_border_width)
        h = int(self.config.image_height + 0.5 * self.config.cai_border_width)
        w = max(h, w)

        return w, h

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, self.config.color_names['white'])

        # bars
        ctx.set_source_rgb(*self.config.osmc_colors['red'])
        ctx.rectangle(0, 0, w, h)
        ctx.set_line_width(self.config.image_border_width)
        ctx.stroke()

        ctx.set_line_width(0)
        bwidth = self.config.cai_border_width
        if self.typ == 'stripe':
            ctx.rectangle(0, 0, bwidth, h)
            ctx.fill()
            ctx.rectangle(w - bwidth, 0, bwidth, h)
            ctx.fill()
        else:
            ctx.rectangle(0, 0, w, 0.9 * bwidth)
            ctx.fill()
            ctx.rectangle(0, h - 0.9 * bwidth, w, 0.9 * bwidth)
            ctx.fill()

        # reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        y = (h - baseh)/2.0
        if self.typ == 'bar':
            y -= 1

        self.render_layout(ctx, layout, color=self.config.text_color,
                           x=(w-tw)/2.0, y=y)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if region != 'it':
        return None

    osmc = re.match('red:red:white_(bar|stripe):([0-9a-zA-Z]+):black',
                    tags.get('osmc:symbol', ''))
    if not osmc:
        return None

    new_config = config.derive(border_color=(1., 1., 1.))
    return CaiHikingSymbol(osmc.group(1), osmc.group(2), new_config)
