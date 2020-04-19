# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from .common.tags import Tags
from .common.config import ShieldConfig
from .common.shield_maker import load_shield_maker

class TagsAll(object):
    """ Restricts the given style to objects which have all
        of the given tags in the tag list.
    """

    def __init__(self, style, tags):
        self.style = load_shield_maker(style)
        self.tags = tags

    def create_for(tags: Tags, region: str, config: ShieldConfig):
        if not tags.matches_tags(self.tags):
            return None

        return self.style.create_for(tags, region, config)


def tags_all(style, filter_tags):
    style_mod = load_shield_maker(style)
    class _TagsAll:
        def create_for(tags: Tags, region: str, config: ShieldConfig):
            if not tags.matches_tags(filter_tags):
                return None

            return style_mod.create_for(tags, region, config)

    return _TagsAll
