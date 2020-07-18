# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from .common.tags import Tags
from .common.config import ShieldConfig
from .common.shield_maker import load_shield_maker

def tags_all(style, filter_tags):
    style_mod = load_shield_maker(style)
    class _TagsAll:
        def create_for(tags: Tags, region: str, config: ShieldConfig):
            if tags.contains_all_tags(filter_tags):
                return style_mod.create_for(tags, region, config)

            return None

    return _TagsAll
