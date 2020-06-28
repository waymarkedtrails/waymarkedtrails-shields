# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from .common.config import ShieldConfig
from .common.tags import Tags
from .common.shield_maker import load_shield_maker

class ShieldFactory(object):
    """ A shield factory renders a shield according to the configured styles.

        `styles` contains the list of styles to be renderable. Order matters.
        When creating a shield maker, the factory returns a shield maker for
        the first style that matches the given tags. A style can be one of three
        formats:

        * A string starting with a dot. The one of the system styles from
          the `styles` directory is used.
        * A string pointing to a loadable module.
        * A style object.

        Both, module and style object must supply a single function
        `create_for(tags: Tags, region: str, config: ShieldConfig)` which
        takes a list of tags, a string describing the region and a pointer
        to the configuration to use. It must return a ShieldMaker object.
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



