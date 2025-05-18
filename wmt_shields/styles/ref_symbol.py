# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker


class RefSymbol(RefShieldMaker):

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref
        self.uuid_pattern = f'ref_{{}}_{self.ref_uuid()}'

    def dimensions(self):
        tw, _ = self._get_text_size(self.config.text_font)
        text_border = self.config.text_border_width or 1.5
        image_border = self.config.image_border_width or 2.5
        w = int(tw + 2 * text_border + 2 * image_border)

        return (w, self.config.image_height or 16)

    def render(self, ctx):
        w, h = self.render_background(ctx, self.config.text_bgcolor)

        # reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        bnd_wd = self.config.text_border_width or 1.5

        self.render_layout(
            ctx, layout, color=self.config.text_color or (0, 0, 0),
            x=(w - tw)/2,
            y=(h - bnd_wd - baseh)/2.0)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.make_ref(names=('name', 'osmc:name'))
    if ref is None:
        return None

    return RefSymbol(ref, config)
