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
from ..common.shield_maker import ShieldMaker

class ColorBoxSymbol(ShieldMaker):
    """ A shield with a typical sign for nordic ski piste.
    """

    def __init__(self, name, color, config):
        self.config = config
        self.color = color
        self.colorname = name

    def uuid(self):
        return "nordic_{}_{}".format(self.config.style or '', self.colorname)

    def render(self, ctx, w, h):
        ctx.arc(w/2, h/2, w/2, 0, 2*pi)
        ctx.set_source_rgb(*self.color)
        ctx.fill()


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if tags.get('piste:type') != 'nordic':
        return None

    color = tags.as_color(('color', 'colour'), config.color_names or {})
    if color is None:
        return None

    return ColorBoxSymbol(*color, config)
