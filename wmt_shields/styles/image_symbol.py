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

class ImageSymbol(ShieldMaker):
    """ A shield with an arbitrary SVG image.
    """

    def __init__(self, uuid, filename, config):
        self.config = config
        self.uuid_pattern = uuid
        if filename.startswith('/'):
            self.filename = filename
        else:
            self.filename = os.path.join(self.config.data_dir, filename)

    def uuid(self):
        return self.uuid_pattern.format(self.config.style or '')

    def render(self, ctx, w, h):
        rhdl = Rsvg.Handle.new_from_file(self.filename)
        dim = rhdl.get_dimensions()

        ctx.scale(w/dim.width, h/dim.height)
        rhdl.render_cairo(ctx)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    for name, stags in config.shield_names.items():
        if tags.matches_tags(stags):
            uuid = 'shield_{}_' + name
            fn = os.path.join(config.shield_path, name + '.svg')
            return ImageSymbol(uuid, fn, config)

    return None
