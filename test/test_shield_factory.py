# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import unittest

from wmt_shields.common.shield_maker import load_shield_maker
from wmt_shields import ShieldFactory
from wmt_shields.styles.ref_symbol import RefSymbol

class Dummy(object):
    pass

class TestLoadShields(unittest.TestCase):

    def test_load_internal(self):
        f = load_shield_maker('.ref_symbol')
        self.assertTrue(hasattr(f, 'RefSymbol'))

    def test_load_external(self):
        f = load_shield_maker('mock_shields')
        self.assertTrue(hasattr(f, 'NullShield'))

    def test_load_class(self):
        f = load_shield_maker(Dummy())
        self.assertIsInstance(f, Dummy)

