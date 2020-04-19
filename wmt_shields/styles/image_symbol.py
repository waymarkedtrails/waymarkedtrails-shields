# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import os

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import ShieldMaker

class ImageSymbol(ShieldMaker):
    """ A shield with an arbitrary SVG image.
    """

    def __init__(self, uuid, filename, config):
        self.config = config
        self.uuid_pattern = uuid
        if filename.startswith('/'):
            self.filename = filename
        else:
            self.filename = os.path.join(self.config.data_dir, filename)

    def render(self, ctx, w, h):
        rhdl = Rsvg.Handle.new_from_file(self.filename)
        dim = rhdl.get_dimensions()

        ctx.scale(w/dim.width, h/dim.height)
        rhdl.render_cairo(ctx)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    for name, stags in config.shield_names.items():
        if tags.matches_tags(stags):
            uuid = f'shield_{{}}_{name}'
            fn = os.path.join(config.shield_path, f'{name}.svg')
            return ImageSymbol(uuid, fn, config)

    return None
