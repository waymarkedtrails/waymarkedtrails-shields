# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann
#
# This is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import re

class Tags(object):
    """ Convenience class for handling OSM tag dictionaries.
    """

    def __init__(self, tags):
        self._tags = tags

    def __getattr__(self, name):
        return getattr(self._tags, name)


    def first_of(self, *params, default=None):
        for key in params:
            if key in self._tags:
                return self._tags[key]

        return default

    def first_starting_with(self, prefix):
        for k, v in self._tags.items():
            if k.startswith(prefix):
                return k, v

        return None, None

    def matches_tags(self, tags):
        for k,v in tags.items():
            if self._tags.get(k) != v:
                return False

        return True

    def make_ref(self, maxlen=5, refs=('ref',), names=('name',)):
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

        if len(name) <= 5:
            return name

        ref = re.sub('[^A-Z]+', '', name)[:min(3, maxlen)]
        if len(ref) < 2:
            ref = re.sub(' ', '', name)[:min(3, maxlen)]

        return ref

    def as_color(self, tags, color_names={}):
        """ Return the first found tag in `tags` as a color description or None
            if none of the tags could be found. The color description is a
            tuple of a RGB tuple and a name.
        """
        color = self.first_of(*tags)
        if color is None:
            return None

        if color in color_names:
            return color, color_names[color]

        m = re.match('#([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$', color)
        if not m:
            return None

        return color[1:], ((1.0+int(m.group(1),16))/256.0,
                           (1.0+int(m.group(2),16))/256.0,
                           (1.0+int(m.group(3),16))/256.0)

