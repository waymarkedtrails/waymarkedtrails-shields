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

from math import pi

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker


class SlopeSymbol(RefShieldMaker):
    """ A shield that resembles typical slope signes.
    """

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref
        if self.config.style:
            self.uuid_prefix = "slope_{}_".format(self.config.style)
        else:
            self.uuid_prefix = "slope_"

    def render(self, ctx, w, h):
        # background fill
        ctx.arc(w/2, h/2, w/2, 0, 2*pi)
        color = self.config.slope_color
        ctx.set_source_rgb(*color)
        ctx.fill()

        # reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        bnd_wd = self.config.text_border_width or 1.5

        self.render_layout(
            ctx, layout, color=self.config.text_color or (0, 0, 0),
            x=(w - tw)/2,
            y=(h - bnd_wd - baseh)/2.0)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if config.style is None or tags.get('piste:type') != 'downhill':
        return None

    ref = tags.make_ref(maxlen=3, refs=('piste:ref',), names=('piste:name')) \
          or tags.make_ref(maxlen=3, refs=('ref',), names=('name')) \
          or ''

    return SlopeSymbol(ref, config)
