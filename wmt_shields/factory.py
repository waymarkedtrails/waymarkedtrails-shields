# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from .common.config import ShieldConfig
from .common.tags import Tags
from .common.shield_maker import load_shield_maker

class ShieldFactory(object):
    """ A shield factory renders a shield according to the configured styles.
    """

    def __init__(self, styles, config):
        self.config = config
        self.styles = [load_shield_maker(style) for style in styles]

    def create(self, tags, region, **kwargs):
        config = ShieldConfig(self.config, kwargs)
        t = Tags(tags)
        for style in self.styles:
            shield = style.create_for(t, region, config)
            if shield is not None:
                return shield

        return None



