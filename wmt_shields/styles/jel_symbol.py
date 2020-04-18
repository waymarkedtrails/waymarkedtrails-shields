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

import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import os

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import ShieldMaker

class JelSymbol(ShieldMaker):
    """ A shield with hiking shields as used in Hungary.
        See https://wiki.openstreetmap.org/wiki/Key:jel.
    """

    def __init__(self, symbol, config):
        self.config = config
        self.symbol = symbol

    def uuid(self):
        return 'jel_{}_{}'.format(self.config.style or '', self.symbol)

    def render(self, ctx, w, h):
        rhdl = Rsvg.Handle.new_from_file(
                os.path.join(self.config.data_dir, self.config.jel_path,
                            "{}.svg".format(self.symbol)))
        dim = rhdl.get_dimensions()

        ctx.scale(w/dim.width, h/dim.height)
        rhdl.render_cairo(ctx)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.get('jel')
    if ref is None or ref not in config.jel_types:
        return None

    return JelSymbol(ref, config)
