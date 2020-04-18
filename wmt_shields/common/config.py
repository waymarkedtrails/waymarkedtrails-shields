# -*- coding: utf-8
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


class ShieldConfig(object):
    """ A shield configuration container.
    """

    def __init__(self, config, extra):
        self._config = config
        self._extra = extra
        self.style = self._getattr_simple('style')

    def derive(self, **kwargs):
        new_extra = dict(self._extra)
        new_extra.update(kwargs)
        return ShieldConfig(self._config, new_extra)

    def __getattr__(self, name):
        if self.style is not None:
            cfg = self._getattr_simple('style_config')

            if cfg is not None and self.style in cfg and name in cfg[self.style]:
                return cfg[self.style][name]

        return self._getattr_simple(name)

    def _getattr_simple(self, name):
        if name in self._extra:
            return self._extra[name]
        if isinstance(self._config, dict) and name in self._config:
            return self._config[name]
        if hasattr(self._config, name):
            return getattr(self._config, name)

        return None

