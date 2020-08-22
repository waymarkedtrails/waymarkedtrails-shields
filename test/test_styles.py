# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

import unittest

from wmt_shields import ShieldFactory
from wmt_shields.common.config import ShieldConfig
from wmt_shields.wmt_config import WmtConfig
from pathlib import Path

base_dir = Path(__file__).parent.parent.resolve()

class NullConfig(ShieldConfig):

    def __init__(self):
        super().__init__({}, {})

class TestStyles(unittest.TestCase):

    def assert_shield(self, shieldmaker, expected_uuid):
        self.assertEqual(expected_uuid, shieldmaker.uuid())
        self.assertGreater(shieldmaker.dimensions()[0], 0)
        self.assertGreater(shieldmaker.dimensions()[1], 0)
        self.assertIsInstance(shieldmaker.dimensions()[0], int)
        self.assertIsInstance(shieldmaker.dimensions()[1], int)
        self.assertIsNotNone(shieldmaker.create_image())

    def test_ref_symbol(self):
        for cfg in (NullConfig(), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.ref_symbol'], cfg)

                self.assertIsNone(f.create({}, ''))

                self.assert_shield(f.create({'ref' : 'A'}, ''), 'ref_None_0041')
                self.assert_shield(f.create({'ref' : '.'}, '', style='red'),
                                   'ref_red_002e')
                self.assert_shield(f.create({'ref' : 'AAAAAAAA'}, ''),
                                   'ref_None_00410041004100410041')

    def test_cai_hiking_symbol(self):
        for cfg in (NullConfig(), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.cai_hiking_symbol'], cfg)

                self.assertIsNone(f.create({}, 'it'))
                self.assertIsNone(f.create({'osmc:symbol' : 'red:red:white_bar:2:black'}, ''))
                self.assertIsNone(f.create({'osmc:symbol' : 'red:red:white_cross:2:black'}, 'it'))

                self.assert_shield(
                    f.create({'osmc:symbol' : 'red:red:white_bar:2:black'}, 'it'),
                             'cai_None_bar_0032')
                self.assert_shield(
                    f.create({'osmc:symbol' : 'red:red:white_stripe:2:black'}, 'it'),
                             'cai_None_stripe_0032')

    def test_color_box(self):
        for cfg in (NullConfig(), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.color_box'], cfg)

                self.assertIsNone(f.create({}, ''))

                self.assert_shield(
                    f.create({'color' : '#f0f0f0'}, ''), 'cbox_None_f0f0f0')

    def test_image_symbol(self):
        for cfg in (NullConfig(), WmtConfig()):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.image_symbol'], cfg)

                self.assertIsNone(f.create({}, ''))

                setattr(cfg, 'shield_names',
                        {'wheel' : {'tag1' : 'foo', 'tag2' : 'bar'}})
                setattr(cfg, 'shield_path', 
                        str(base_dir / 'wmt_shields' / 'data' / 'osmc'))

                f = ShieldFactory(['.image_symbol'], cfg)

                self.assertIsNone(f.create({'tag1' : 'foo'}, ''))

                self.assert_shield(
                    f.create({'tag1' : 'foo', 'tag2' : 'bar'}, ''),
                    'shield_None_wheel')

    def test_jel_symbol(self):
        f = ShieldFactory(['.jel_symbol'], NullConfig())
        self.assertIsNone(f.create({'jel' : 'flo'}, ''))

        mincfg = ShieldConfig({'jel_types' : ('flo', ), 'jel_path' : '{data}/jel'}, {})
        for cfg in (mincfg, WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.jel_symbol'], cfg)

                self.assertIsNone(f.create({}, ''))
                self.assertIsNone(f.create({'jel' : 'xx233ssdd'}, ''))

                self.assert_shield(
                    f.create({'jel' : 'flo'}, ''), 'jel_None_flo')

    def test_kct_symbol(self):
        f = ShieldFactory(['.kct_symbol'], NullConfig())
        self.assertIsNone(f.create({'kct_major' : 'red'}, ''))

        mincfg = ShieldConfig({'kct_types' : ('major', ),
                               'kct_colors' : {'red' : (1, 0, 0)},
                               'kct_path' : '{data}/kct'}, {})
        for cfg in (mincfg, WmtConfig):
            f = ShieldFactory(['.kct_symbol'], cfg)

            self.assertIsNone(f.create({'operator' : 'kst', 'colour' : 'red'}, ''))
            self.assertIsNone(f.create({'operator' : 'kst', 'symbol' : 'major'}, ''))
            self.assertIsNone(f.create({'symbol' : 'major', 'colour' : 'red'}, ''))

            self.assert_shield(
                f.create({'operator' : 'kst', 'colour' : 'red', 'symbol' : 'major'}, ''),
                'kct_None_red-major')
            self.assert_shield(
                f.create({'kct_red' : 'major'}, ''),
                'kct_None_red-major')

    def test_nordic_symbol(self):
        for cfg in (NullConfig(), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.nordic_symbol'], cfg)

                self.assertIsNone(f.create({'color' : '#f0f0f0'}, ''))
                self.assertIsNone(f.create({'piste:type' : 'nordic'}, ''))

                self.assert_shield(
                    f.create({'piste:type' : 'nordic', 'color' : '#f0f0f0'}, ''),
                    'nordic_None_f0f0f0')


    def test_osmc_symbol(self):
        f = ShieldFactory(['.osmc_symbol'], NullConfig())
        self.assertIsNone(f.create({'osmc:symbol' : 'black::black_stripe'}, ''))

        mincfg = ShieldConfig({'osmc_colors' : WmtConfig.osmc_colors,
                               'osmc_path' : '{data}/osmc'}, {})
        for cfg in (mincfg, WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.osmc_symbol'], cfg)

                self.assertIsNone(f.create({}, ''))

                for fg in ('arch', 'backslash', 'bar', 'circle', 'corner', 'cross',
                           'diamond_line', 'diamond', 'dot', 'fork', 'lower',
                           'right', 'pointer', 'rectangle_line', 'rectangle',
                           'red_diamond', 'slash', 'stripe', 'triangle_line',
                           'triangle', 'triangle_turned', 'turned_T', 'x',
                           'hexagon', 'shell', 'shell_modern', 'hiker', 'wheel'):
                    self.assert_shield(
                        f.create({'osmc:symbol' : f'black::black_{fg}'}, ''),
                        f'osmc_None_empty_{fg}_black')

                for bg in ('circle', 'frame', 'round'):
                    self.assert_shield(
                        f.create({'osmc:symbol' : f'black:red_{bg}'}, ''),
                        f'osmc_None_red_{bg}')

                self.assert_shield(
                        f.create({'osmc:symbol' : 'white:black::45:black'}, ''),
                        'osmc_None_black_00340035_black')
                self.assert_shield(
                        f.create({'osmc:symbol' : 'white:black:blue_stripe:orange_stripe_right'} , ''),
                        'osmc_None_black_stripe_blue_orange')
                self.assert_shield(
                        f.create({'osmc:symbol' : 'white:black:wheel'}, ''),
                        'osmc_None_black_wheel_black')


    def test_ref_color_symbol(self):
        for cfg in (ShieldConfig({'colorbox_names' : WmtConfig.colorbox_names}, {}), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.ref_color_symbol'], cfg)

                self.assertIsNone(f.create({'ref' : 'A'}, ''))
                self.assertIsNone(f.create({'color' : '#eeeeee'}, ''))
                self.assertIsNone(f.create({'ref' : 'A', 'color' : 'greenish'}, ''))

                self.assert_shield(f.create({'ref' : 'A', 'color' : '#eeeeee'}, ''),
                                   'ctb_None_eeeeee_0041')
                self.assert_shield(f.create({'ref' : 'AAAAAAAA', 'color' : '#101010'}, ''),
                                   'ctb_None_101010_00410041004100410041')
                self.assert_shield(f.create({'ref' : 'A', 'color' : 'red'}, ''),
                                   'ctb_None_red_0041')


    def test_slope_symbol(self):
        for cfg in (ShieldConfig({'slope_colors' : WmtConfig.slope_colors}, {}), WmtConfig):
            with self.subTest(i=cfg):
                f = ShieldFactory(['.slope_symbol'], cfg)

                self.assertIsNone(f.create({}, ''))

                self.assert_shield(
                    f.create({'piste:type' : 'downhill'}, '', difficulty=0),
                    'slope_None_0')
                self.assert_shield(
                    f.create({'piste:type' : 'downhill', 'piste:ref' : 'A'}, '', difficulty=9),
                    'slope_None_9_0041')

    def test_swiss_mobile(self):
        f = ShieldFactory(['.swiss_mobile'], WmtConfig)

        self.assertIsNone(f.create({'ref' : '23'}, ''))
        self.assertIsNone(f.create({'operator' : 'Swiss mobility'}, ''))
        self.assertIsNone(f.create({'ref' : '0', 'operator' : 'Swiss mobility'}, ''))

        self.assert_shield(
            f.create({'operator' : 'Swiss mobility', 'network' : 'nwn', 'ref' : '7'} , ''),
            'swiss_None_0037')

