# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import os

from ..common.tags import Tags
from ..common.config import ShieldConfig
from .image_symbol import ImageSymbol

def create_for(tags: Tags, region: str, config: ShieldConfig):
    ref = tags.get('jel')
    if ref is None or ref not in config.jel_types:
        return None

    uuid = f'jel_{{}}_{ref}'
    return ImageSymbol(uuid, config.jel_path, f'{ref}.svg', config)
