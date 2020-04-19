# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

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



