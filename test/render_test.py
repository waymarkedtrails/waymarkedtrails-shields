# -*- coding: utf-8
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

"""
Renders various shields for testing
"""
import os
import sys
from wmt_shields import ShieldFactory
from wmt_shields.wmt_config import WmtConfig
import wmt_shields.filters as filters

class GlobalConfig(WmtConfig):
    shield_path = '{data}/osmc'
    shield_names = { 'wheel' : {'operator':'wheely'},}

    style_config = dict(
                    novice= { 'slope_color' : (0.7, 0.01, 0.01), },
                    **WmtConfig.style_config)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python symbol.py <outdir>")
        sys.exit(-1)

    conf = GlobalConfig()

    factory = ShieldFactory(
                ('.slope_symbol',
                 '.nordic_symbol',
                 '.image_symbol',
                 '.cai_hiking_symbol',
                 '.swiss_mobile',
                 '.jel_symbol',
                 '.kct_symbol',
                 '.osmc_symbol',
                 '.ref_color_symbol',
                 '.ref_symbol',
                 filters.tags_all('.color_box',
                                  {'operator' : 'Norwich City Council',}),
                 '.color_box'
                ), conf)

    # Testing
    outdir = sys.argv[1]
    testsymbols = [
        ('INT', '', { 'operator':'wheely'}),
        ('INT', '', { 'ref' : '10' }),
        ('LOC', '', { 'ref' : '15' }),
        ('REG', '', { 'ref' : 'WWWW' }),
        ('NAT', '', { 'ref' : '1' }),
        ('REG', '', { 'ref' : 'Ag' }),
        ('REG', '', { 'ref' : u'１号路' }),
        ('REG', '', { 'ref' : u'يلة' }),
        ('REG', '', { 'ref' : u'하이' }),
        ('REG', '', { 'ref' : u'шие' }),
        ('NAT', '', { 'ref' : '7', 'operator' : 'swiss mobility', 'network' : 'nwn'}),
        ('REG', '', { 'ref' : '57', 'operator' : 'swiss mobility', 'network' : 'rwn'}),
        ('REG', '', { 'operator' : 'kst', 'symbol' : 'learning', 'colour' : 'red'}),
        ('INT', '', { 'osmc:symbol' : 'red::blue_lower' }),
        ('INT', '', { 'osmc:symbol' : 'white:white:blue_lower' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_arch' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_backslash' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_bar' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_circle' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_cross' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_diamond_line' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:red_diamond' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_dot' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_fork' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_pointer' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_rectangle_line' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_rectangle' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_red_diamond' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_slash' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_stripe' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_triangle_line' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_triangle' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_triangle_turned' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_turned_T' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:blue_x' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:red_hexagon' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white_circle:yellow_triangle' }),
        ('LOC', '', { 'osmc:symbol' : 'white:black_frame:blue_x' }),
        ('LOC', '', { 'osmc:symbol' : 'white:red_frame:black_corner' }),
        ('LOC', '', { 'osmc:symbol' : 'white:red_circle:black_corner' }),
        ('LOC', '', { 'osmc:symbol' : 'red:white:red_diamond_line:Tk9:red' }),
        ('INT', '', { 'osmc:symbol' : 'white:blue_frame:red_dot:A' }),
        ('NAT', '', { 'osmc:symbol' : 'white:red:white_bar:222' }),
        ('NAT', '', { 'osmc:symbol' : 'white:red:white_bar:2223' }),
        ('REG', '', { 'osmc:symbol' : 'white:white:shell' }),
        ('LOC', '', { 'osmc:symbol' : 'white:blue:shell_modern' }),
        ('LOC', '', { 'osmc:symbol' : 'white:white:hiker' }),
        ('LOC', '', { 'osmc:symbol' : 'white::green_hiker' }),
        ('LOC', '', { 'osmc:symbol' : 'white::blue_hiker' }),
        ('LOC', '', { 'osmc:symbol' : 'white::blue_wheel' }),
        ('LOC', '', { 'osmc:symbol' : 'white::red_wheel' }),
        ('LOC', '', { 'osmc:symbol' : 'white::wheel' }),
        ('LOC', '', { 'osmc:symbol' : 'white:brown:white_triangle' }),
        ('LOC', '', { 'osmc:symbol' : 'white:gray:purple_fork' }),
        ('LOC', '', { 'osmc:symbol' : 'white:green:orange_cross' }),
        ('LOC', '', { 'osmc:symbol' : 'white:orange:black_lower' }),
        ('LOC', '', { 'osmc:symbol' : 'white:orange:black_right' }),
        ('LOC', '', { 'osmc:symbol' : 'white:purple:green_turned_T' }),
        ('LOC', '', { 'osmc:symbol' : 'white:red:gray_stripe'}),
        ('LOC', '', { 'osmc:symbol' : 'white:yellow:brown_diamond_line'}),
        ('LOC', '', { 'osmc:symbol' : 'red:white:red_wheel'}),
        ('LOC', '', { 'osmc:symbol' : 'red:white:red_corner'}),
        ('REG', '', { 'osmc:symbol' : 'green:green_frame::L:green'}),
        ('REG', '', { 'osmc:symbol' : 'green:green_circle:green_dot'}),
        ('REG', '', { 'osmc:symbol' : 'green:white:green_dot'}),
        ('REG', '', { 'osmc:symbol' : 'green:red_round::A:white'}),
        ('REG', '', { 'osmc:symbol' : 'green:red_round::j:white'}),
        ('REG', '', { 'osmc:symbol' : 'blue:white::Lau:blue'}),
        ('NAT', '', { 'osmc:symbol' : 'yellow:brown_round:red_dot'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:223:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:1434:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:1:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:1:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:26:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:26:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:26s:black'}),
        ('REG', 'it', { 'osmc:symbol' : 'red:red:white_stripe:AVG:black'}),
        ('REG', 'it', { 'osmc:symbol' : 'white:black:blue_stripe:orange_stripe_right'}),
        ('LOC', '', { 'jel' : 'p+', 'ref' : 'xx'}),
        ('LOC', '', { 'jel' : 'foo', 'ref' : 'yy'}),
        ('LOC', '', { 'kct_red' : 'major'}),
        ('LOC', '', { 'kct_green' : 'interesting_object'}),
        ('LOC', '', { 'kct_yellow' : 'ruin'}),
        ('LOC', '', { 'kct_blue' : 'spring'}),
        ('LOC', '', { 'operator' : 'Norwich City Council', 'color' : '#FF0000'}),
        ('LOC', '', { 'operator' : 'Norwich City Council', 'colour' : '#0000FF'}),
        ('LOC', '', { 'ref' : '123', 'colour' : 'yellow'}),
        ('NAT', '', { 'ref' : 'KCT', 'colour' : 'blue'}),
        ('NAT', '', { 'ref' : 'YG4E3', 'colour' : 'green'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'aqua'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'black'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'blue'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'brown'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'green'}),
        ('NAT', '', { 'ref' : 'X/XX', 'colour' : 'grey'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'maroon'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'orange'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'pink'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'purple'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'red'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'violet'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'white'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : 'yellow'}),
        ('NAT', '', { 'ref' : 'XXX', 'colour' : '#ee0000'}),
        ('downhill', '', { 'piste:type' : 'nordic', 'colour' : '#0000FF'}),
        ('novice', '', { 'piste:type' : 'downhill', 'piste:difficulty' : 'novice'}),
        ('novice', '', { 'piste:type' : 'downhill', 'piste:ref' : 'XX'}),
    ]

    for level, region, tags in testsymbols:
        sym = factory.create(tags, region, style=level)
        if sym is None:
            print("Unknown tags:", tags)
            continue

        sym.to_file(os.path.join(outdir, sym.uuid() + '.svg'), format='svg')
