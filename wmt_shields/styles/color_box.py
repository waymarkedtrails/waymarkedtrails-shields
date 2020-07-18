# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import ShieldMaker

class ColorBoxSymbol(ShieldMaker):
    """ A shield with nothing but a background color.
    """

    def __init__(self, color, config):
        self.config = config
        self.color = color.rgb
        self.uuid_pattern = f'cbox_{{}}_{color.name}'

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, self.color)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    color = tags.as_color(color_names=config.color_names or {})
    if color is None:
        return None

    return ColorBoxSymbol(color, config)
