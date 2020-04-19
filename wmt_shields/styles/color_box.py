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
from ..common.shield_maker import ShieldMaker

class ColorBoxSymbol(ShieldMaker):
    """ A shield with nothing but a background color.
    """

    def __init__(self, name, color, config):
        self.config = config
        self.color = color
        self.uuid_pattern = f'cbox_{{}}_{name}'

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, self.color)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    color = tags.as_color(('color', 'colour'), config.color_names or {})
    if color is None:
        return None

    return ColorBoxSymbol(*color, config)
