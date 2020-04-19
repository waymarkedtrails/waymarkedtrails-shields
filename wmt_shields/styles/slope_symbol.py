# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from math import pi

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker


class SlopeSymbol(RefShieldMaker):
    """ A shield that resembles typical slope signes.
    """

    def __init__(self, ref, config):
        self.config = config
        self.ref = ref
        self.uuid_pattern = f'slope_{{}}_{self.ref_uuid()}'

    def render(self, ctx, w, h):
        # background fill
        ctx.arc(w/2, h/2, w/2, 0, 2*pi)
        color = self.config.slope_color
        ctx.set_source_rgb(*color)
        ctx.fill()

        # reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        bnd_wd = self.config.text_border_width or 1.5

        self.render_layout(
            ctx, layout, color=self.config.text_color or (0, 0, 0),
            x=(w - tw)/2,
            y=(h - bnd_wd - baseh)/2.0)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    if config.style is None or tags.get('piste:type') != 'downhill':
        return None

    ref = tags.make_ref(maxlen=3, refs=('piste:ref',), names=('piste:name')) \
          or tags.make_ref(maxlen=3, refs=('ref',), names=('name')) \
          or ''

    return SlopeSymbol(ref, config)
