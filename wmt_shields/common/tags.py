# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import re
from dataclasses import dataclass
from typing import Dict, Sequence

@dataclass
class Tag:
    k: str
    v: str

@dataclass
class OsmColor:
    name: str
    rgb: str


class Tags(object):
    """ Convenience class for handling OSM tag dictionaries.
    """

    def __init__(self, tags: Dict[str, str]):
        self._tags = tags

    def __getattr__(self, name: str):
        return getattr(self._tags, name)


    def first_of(self, *keys, default: str=None) -> str:
        """ Return the first value for a list of keys. If none of the
            keys is available, return the `default` value.
        """
        for key in keys:
            if key in self._tags:
                return self._tags[key]

        return default

    def starting_with(self, prefix: str) -> Tag:
        """ Return a tag whose key starts with the given `prefix`. If no such
            tag is found, return 'None'. If multiple tags start with the
            prefix, then one of them is returned at random.
        """
        for k, v in self._tags.items():
            if k.startswith(prefix):
                return Tag(k, v)

        return None

    def contains_all_tags(self, tags) -> bool:
        """ Return True when all tags in the list of tags are contained
            in the list of tags.
        """
        if isinstance(tags, dict):
            tags = tags.items()

        for k, v in tags:
            if self._tags.get(k) != v:
                return False

        return True

    def make_ref(self, maxlen: int=5, refs=('ref',), names=('name',)):
        """ Return a reference for the object. The function looks first for
            a true reference tag from `refs`. If one is found, it is shortened
            to `maxlen` and returned. If none is found, it looks for a
            name tag from `names` and shortens the name by using the initials.
        """
        ref = self.first_of(*refs)
        if ref is not None:
            return re.sub(' ', '', ref)[:maxlen]

        # try some magic with the name
        name = self.first_of(*names)
        if name is None:
            return None

        if len(name) <= maxlen:
            return name

        ref = ''.join(filter(lambda c: c.isdigit() or c.isupper(), name))[:maxlen]
        if len(ref) < 2:
            ref = re.sub(' ', '', name)[:maxlen]

        return ref

    def as_color(self, keys: Sequence[str]=('color', 'colour'),
                 color_names: dict=None) -> OsmColor:
        """ Return the first found tag with a key from `keys` as a color
            description. If no tag can be found or the tag value is not a valid
            color return `None`. The color description may either be a color
            name or a HTML color key. Valid names and their translation to
            RGB
            or None
            if none of the tags could be found. The color description is a
            tuple of a RGB tuple and a name.
        """
        color = self.first_of(*keys)
        if color is None:
            return None

        if color_names is not None and color in color_names:
            return OsmColor(color, color_names[color])

        m = re.match('#([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$', color)
        if not m:
            return None

        return OsmColor(color[1:], ((1.0+int(m.group(1),16))/256.0,
                                   (1.0+int(m.group(2),16))/256.0,
                                   (1.0+int(m.group(3),16))/256.0))

