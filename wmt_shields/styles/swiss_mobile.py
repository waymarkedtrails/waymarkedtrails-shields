# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class SwissMobileSymbol(RefShieldMaker):
    """ A shield in the style of the Swiss Mobile hiking/cycling network.
    """

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref.strip()[:5]
        self.uuid_pattern = f'swiss_{{}}_{self.ref_uuid()}'

    def dimensions(self):
        return 8 + len(self.ref) * 7, self.config.image_height or 16

    def render(self, ctx):
        w, h = self.render_background(ctx, self.config.swiss_mobile_bgcolor)

        layout, tw, baseh = self.layout_ref(ctx, self.config.swiss_mobile_font)

        bwidth = self.config.image_border_width/2.0

        self.render_layout(ctx, layout, color=self.config.swiss_mibile_color,
                           x=w - tw - bwidth, y=h - baseh - bwidth)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.get('ref')
    if ref is None:
        return None
    if tags.get('operator', '').lower() not in config.swiss_mobile_operators:
        return None
    if tags.get('network', '') not in config.swiss_mobile_networks:
        return None

    return SwissMobileSymbol(ref, config)
