# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

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

