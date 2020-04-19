# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

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
        self.uuid_pattern = f'nordic_{{}}_{name}'

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
