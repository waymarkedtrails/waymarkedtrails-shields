# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2020 Sarah Hoffmann

import unittest

from wmt_shields.common.tags import Tag, Tags, OsmColor

class TestTags(unittest.TestCase):

    def test_getattr(self):
        tags = Tags({'highway': 'road', 'name': 'A1', 'ref': '10'})

        self.assertEqual('road', tags.get('highway'))
        self.assertEqual('default', tags.get('foo', 'default'))

    def test_firstof(self):
        tags = Tags({'building': 'house', 'roof': 'no', 'wall': 'yes'})

        self.assertEqual('no', tags.first_of('roof', 'wall'))
        self.assertEqual('no', tags.first_of('window', 'roof'))

        self.assertIsNone(tags.first_of('window'))
        self.assertEqual('unavailable', tags.first_of('window', default='unavailable'))

    def test_first_starting_with(self):
        tags = Tags({'name' : 'simple', 'name:de': 'einfach', 'ref': '23'})

        self.assertEqual('name:de', tags.starting_with('name:').k)
        self.assertIn(tags.starting_with('name').v, ('simple', 'einfach'))
        self.assertIsNone(tags.starting_with('ref:'))

    def test_contains_all_tags(self):
        tags = Tags({'amenity': 'restaurant', 'tourism': 'hotel', 'name': 'F2'})

        self.assertTrue(tags.contains_all_tags({'name': 'F2'}))
        self.assertTrue(tags.contains_all_tags({'name': 'F2', 'tourism': 'hotel'}))
        self.assertFalse(tags.contains_all_tags({'name': 'F2a'}))
        self.assertFalse(tags.contains_all_tags({'amenity': 'restaurant', 'name': 'F2a'}))
        self.assertTrue(tags.contains_all_tags({}))

        self.assertTrue(tags.contains_all_tags((('amenity', 'restaurant'), )))
        self.assertFalse(tags.contains_all_tags((('foo', 'bar'), )))


    def test_make_ref(self):
        self.assertEqual('1', Tags({'ref': '1'}).make_ref())
        self.assertEqual('x', Tags({'ref': ' x '}).make_ref())
        self.assertEqual('123', Tags({'ref': '12345'}).make_ref(maxlen=3))
        self.assertEqual('12345', Tags({'ref': '123456'}).make_ref())

        self.assertEqual('A', Tags({'ref': '1', 'id': 'A'}).make_ref(refs=('id', 'ref')))

        self.assertEqual('Au', Tags({'name': 'Au'}).make_ref())
        self.assertEqual('MGR', Tags({'name': 'MyGardenRoute'}).make_ref())
        self.assertEqual('small', Tags({'name': 'small caps everywhere'}).make_ref())
        self.assertEqual('Abc', Tags({'name': 'Abcde'}).make_ref(maxlen=3))
        self.assertEqual('AC', Tags({'name': 'Axx bxx Cxx'}).make_ref())
        self.assertEqual('AAA', Tags({'name': 'Ax Ay Az Bf'}).make_ref(maxlen=3))

        self.assertEqual('X1', Tags({'name:de': 'Xanten 1', 'name': 'unknown'})
                                 .make_ref(names=('name:de', 'name')))

        self.assertIsNone(Tags({'foo': 'bar'}).make_ref())

    def test_as_color(self):
        self.assertIsNone(Tags({'foo': 'bar'}).as_color(('color',)))

        self.assertIsNone(Tags({'color': '121212'}).as_color())
        self.assertIsNone(Tags({'color': 'red'}).as_color())

        self.assertEqual(OsmColor('ffffff', (1.0, 1.0, 1.0)),
                         Tags({'colour': '#ffffff'}).as_color())
        self.assertEqual(OsmColor('red', (1.0, 0, 0)),
                         Tags({'color': 'red'}).as_color(color_names={'red': (1.0, 0, 0)}))
