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

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker


class RefSymbol(RefShieldMaker):

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref
        self.uuid_pattern = f'ref_{{}}_{self.ref_uuid()}'

    def dimensions(self):
        tw, _ = self._get_text_size(self.config.text_font)
        text_border = self.config.text_border_width or 1.5
        image_border = self.config.image_border_width or 2.5
        w = int(tw + 2 * text_border + 2 * image_border)

        return (w, self.config.image_height or 16)

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, self.config.text_bgcolor)

        # reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        bnd_wd = self.config.text_border_width or 1.5

        self.render_layout(
            ctx, layout, color=self.config.text_color or (0, 0, 0),
            x=(w - tw)/2,
            y=(h - bnd_wd - baseh)/2.0)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.make_ref(names=('name', 'osmc:name'))
    if ref is None:
        return None

    return RefSymbol(ref, config)
