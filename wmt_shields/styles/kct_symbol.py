# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import re
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import os

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import ShieldMaker

class KctSymbol(ShieldMaker):
    """ A shield with hiking shields as used by the Czech and Slovakian
        hiking clubs.
        See https://wiki.openstreetmap.org/wiki/Key:kct_red.
    """

    def __init__(self, color, symbol, config):
        self.config = config
        self.uuid_pattern = f'kct_{{}}_{color}-{symbol}'
        self.color = color
        self.symbol = symbol

    def dimensions(self):
        bwidth = self.config.image_border_width or 0
        return ((self.config.image_width or 16) + 0.5 * bwidth,
                (self.config.image_height or 16) + 0.5 * bwidth)

    def render(self, ctx, w, h):
        # get the template file
        content = self.find_resource(self.config.kct_path, f'{self.symbol}.svg').decode('utf8')
        # patch in the correct color
        fgcol = tuple([int(x*255) for x in self.config.kct_colors[self.color]])
        color = '#%02x%02x%02x' % fgcol
        content = re.sub('#eeeeee', color, content)
        # now read in by cairo
        svg = Rsvg.Handle.new_from_data(content.encode())
        dim = svg.get_dimensions()

        ctx.scale(w/dim.width, h/dim.height)
        svg.render_cairo(ctx)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    # slovakian system
    if tags.get('operator', '').lower() == 'kst':
        col = tags.get('colour')
        sym = tags.get('symbol')
        if  col in config.kct_colors and sym in config.kct_types:
            return KctSymbol(col, sym, config)

    # Czech system
    k, v = tags.first_starting_with('kct_')
    if k is not None and k[4:] in config.kct_colors and v in config.kct_types:
        return KctSymbol(k[4:], v, config)

    return None
