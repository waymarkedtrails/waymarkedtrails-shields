# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import unittest

from wmt_shields.common.config import ShieldConfig

class TestConfig(unittest.TestCase):

    def test_empty_config(self):
        s = ShieldConfig({}, {})

        self.assertIsNone(s.style)
        self.assertIsNone(s.foo)

    def test_style_setting(self):
        self.assertEqual('main', ShieldConfig({'style' : 'main'}, {}).style)
        self.assertEqual('extra', ShieldConfig({}, {'style' : 'extra'}).style)
        self.assertEqual('extra', ShieldConfig({'style' : 'main'},
                                               {'style' : 'extra'}).style)

    def test_config_as_class(self):
        class SomeConfig:
            someattr = 34

        self.assertEqual(34, ShieldConfig(SomeConfig, {}).someattr)
        self.assertEqual(34, ShieldConfig(SomeConfig(), {}).someattr)
        self.assertEqual(None, ShieldConfig(SomeConfig, {'someattr' : None}).someattr)

    def test_derive(self):
        s = ShieldConfig({'orig' : (1, 2, 3)}, {})

        self.assertEqual((1, 2, 3), s.orig)
        self.assertEqual((1, 2, 3), s.derive(newattr='something').orig)
        self.assertEqual('new value', s.derive(orig='new value').orig)

    def test_attribute_from_style(self):
        cfg = { 'X' : {'attr' : 3}}
        self.assertEqual(2, ShieldConfig({'style' : 'X'}, {'attr' : 2}).attr)
        self.assertEqual(2, ShieldConfig({'style' : 'X', 'style_config' : {}},
                                         {'attr' : 2}).attr)
        self.assertEqual(3, ShieldConfig({'style' : 'X', 'style_config' : cfg},
                                         {'attr' : 2}).attr)

