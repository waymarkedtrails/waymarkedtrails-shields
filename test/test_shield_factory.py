# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import unittest
from pathlib import Path

from wmt_shields.common.shield_maker import load_shield_maker, ShieldMaker
from wmt_shields.common.config import ShieldConfig
from wmt_shields import ShieldFactory
from wmt_shields.styles.ref_symbol import RefSymbol

test_dir = Path(__file__).parent.resolve()

class Dummy(object):
    pass

class NullConfig(ShieldConfig):

    def __init__(self):
        super().__init__({}, {})

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

    def test_unknown_module(self):
        with self.assertRaises(ImportError):
            load_shield_maker('foo')


class TestBaseShieldMaker(unittest.TestCase):

    def test_uuid_from_pattern_with_style(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(style='something')
                self.uuid_pattern = "__{}__"

        self.assertEqual("__something__", TestShield().uuid())


    def test_uuid_from_pattern_without_style(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig()
                self.config.style = None
                self.uuid_pattern = "X+{}"

        self.assertEqual("X+None", TestShield().uuid())

    def test_dimensions(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(image_width=55, image_height=8)

        self.assertEqual((55, 8), TestShield().dimensions())

    def test_dimensions_missing_width(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(image_height=100)

        self.assertEqual((16, 100), TestShield().dimensions())

    def test_dimensions_missing_height(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(image_width=1)

        self.assertEqual((1, 16), TestShield().dimensions())

    def test_find_resource_from_file_system(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(data_dir=str(test_dir / '..'))

        t = TestShield()

        self.assertEqual(b'TEST\n',
                         t.find_resource(None, str(test_dir / 'test.res')))
        self.assertEqual(b'TEST\n',
                         t.find_resource('/foo', str(test_dir / 'test.res')))
        self.assertEqual(b'TEST\n',
                         t.find_resource(str(test_dir), 'test.res'))
        self.assertEqual(b'TEST\n',
                         t.find_resource('test', 'test.res'))

        with self.assertRaises(FileNotFoundError):
            t.find_resource(str(test_dir), 'somethingveryunlikelynamexxx56423')

    def test_find_resource_internal(self):
        class TestShield(ShieldMaker):
            def __init__(self):
                self.config = NullConfig().derive(data_dir='{data}/osmc')

        t = TestShield()

        self.assertEqual(1298, len(t.find_resource('{data}', 'osmc/hiker.svg')))
        self.assertEqual(1298, len(t.find_resource(None, 'hiker.svg')))
