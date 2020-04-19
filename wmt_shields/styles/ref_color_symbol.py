# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import RefShieldMaker

class RefColorSymbol(RefShieldMaker):
    """ A shield with a reference with a colored underline according to the
        color tag.
    """

    def __init__(self, ref, name, color, config):
        self.config = config
        self.ref = ref
        self.color = color
        self.uuid_pattern = f'ctb_{{}}_{name}_{self.ref_uuid()}'

    def dimensions(self):
        tw, _ = self._get_text_size(self.config.text_font)
        text_border = self.config.text_border_width or 1.5
        image_border = self.config.image_border_width or 2.5
        w = int(tw + 2 * text_border + 2 * image_border)
        h = int((self.config.image_height or 16) + image_border)
        return (w, h)

    def render(self, ctx, w, h):
        self.render_background(ctx, w, h, (1., 1., 1.))

        image_border = self.config.image_border_width or 2.5

        # bar with halo
        ctx.set_line_width(0)
        ctx.set_source_rgb(*self.color[1])
        ctx.rectangle(image_border + 1.8, h - 3.2 - image_border,
                      w - 2 * (image_border + 1.8) , 3.4)
        ctx.fill()
        ctx.set_source_rgb(*self.color[0])
        ctx.rectangle(image_border + 2, h - 3 - image_border,
                      w - 2 * (image_border + 2) , 3)
        ctx.fill()

        ## reference text
        layout, tw, baseh = self.layout_ref(ctx, self.config.text_font)

        bnd_wd = self.config.text_border_width or 1.5

        self.render_layout(ctx, layout, color=self.config.text_color or (0, 0, 0),
                           x=(w - tw)/2, y=(h - bnd_wd - baseh)/2.0)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.make_ref(names=('name', 'osmc:name'))
    if ref is None:
        return None

    color = tags.as_color(('color', 'colour'), config.colorbox_names or {})
    if color is None:
        return None

    if color[0].startswith('#'):
        return RefColorSymbol(ref, color[0], (color[1], (1., 1., 1.)), config)

    return RefColorSymbol(ref, *color, config)
