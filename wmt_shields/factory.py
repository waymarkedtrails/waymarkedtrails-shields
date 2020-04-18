# -*- coding: utf-8
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

import sys

from .common.config import ShieldConfig
from .common.tags import Tags

class ShieldFactory(object):
    """ A shield factory renders a shield according to the configured styles.
    """

    def __init__(self, styles, config):
        self.config = config
        self.styles = []
        for style in styles:
            if isinstance(style, str):
                if style.startswith('.'):
                    style = 'wmt_shields.styles' + style
                obj = {}
                try:
                    __import__(style)
                    self.styles.append(sys.modules[style])
                except ImportError:
                    print("Style '{}' not found.".format(style))
                    raise
            else:
                self.styles.append(style)


    def create(self, tags, region, **kwargs):
        config = ShieldConfig(self.config, kwargs)
        t = Tags(tags)
        for style in self.styles:
            shield = style.create_for(t, region, config)
            if shield is not None:
                return shield

        return None



