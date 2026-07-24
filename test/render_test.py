# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2025 Sarah Hoffmann

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


OSMC_BACKGROUNDS = ('', '_circle', '_frame', '_round', '_diamond', '_diamond_line')
OSMC_FOREGROUNDS = ("_arch", "_backslash", "_bar", "_circle", "_corner", "_corner_left", "_cross", "_diamond_line", "_diamond", "_diamond_left", "_diamond_right", "_dot", "_fork", "_lower", "_upper", "_right", "_left", "_pointer", "_right_pointer", "_left_pointer", "_pointer_line", "_right_pointer_line", "_left_pointer_line", "_rectangle_line", "_rectangle", "_slash", "_stripe", "_triangle_line", "_triangle", "_triangle_turned", "_turned_T", "_x", "_hexagon", "_shell", "_shell_modern", "_crest", "_arrow", "_right_arrow", "_left_arrow", "_up_arrow", "_down_arrow", "_bowl", "_upper_bowl", "_house", "_L", "_drop", "_drop_line")

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
        ('REG', '', { 'ref' : u'NeyY🟡' }),
        ('REG', '', { 'ref' : u'[⛓' }),
        ('NAT', '', { 'ref' : '7', 'operator' : 'swiss mobility', 'network' : 'nwn'}),
        ('REG', '', { 'ref' : '57', 'operator' : 'swiss mobility', 'network' : 'rwn'}),
        ('REG', '', { 'operator' : 'kst', 'symbol' : 'learning', 'colour' : 'red'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:223:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:1434:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:1:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:1:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_bar:26:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:26:black'}),
        ('LOC', 'it', { 'osmc:symbol' : 'red:red:white_stripe:26s:black'}),
        ('REG', 'it', { 'osmc:symbol' : 'red:red:white_stripe:AVG:black'}),
        ('REG', '', { 'osmc:symbol' : 'white:black:orange_right:blue_stripe'}),
        ('REG', '', { 'osmc:symbol' : 'white:blue_circle::A:black'}),
        ('REG', '', { 'osmc:symbol' : 'white:blue_round::ABCD:white'}),
        ('REG', '', { 'osmc:symbol' : 'white:yellow_diamond:red_diamond'}),
        ('REG', '', { 'osmc:symbol' : 'white:yellow_diamond::A:red'}),
        ('REG', '', { 'osmc:symbol' : 'white:blue_stripe:yellow_lower'}),
        ('REG', '', { 'osmc:symbol' : 'white:gray_bar:black_right'}),
        ('REG', '', { 'osmc:symbol' : 'white:purple_diamond_line:gray_hexagon'}),
        ('REG', '', { 'osmc:symbol' : 'white:black_bar:orange_right:blue_stripe'}),
        ('LOC', '', { 'jel' : 'foo', 'ref' : 'yy'}),
        ('LOC', '', { 'kct_red' : 'major'}),
        ('LOC', '', { 'kct_green' : 'interesting_object'}),
        ('LOC', '', { 'kct_yellow' : 'ruin'}),
        ('LOC', '', { 'kct_blue' : 'spring'}),
        ('LOC', '', { 'kct_blue' : 'horse'}),
        ('LOC', '', { 'kct_blue' : 'learning'}),
        ('LOC', '', { 'kct_blue' : 'peak'}),
        ('LOC', '', { 'kct_blue' : 'local'}),
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

    JEL = ["3","4","atl","atlv","bfk","bor","b","but","c","eml","f3","f4",
           "fatl","fatlv","fbor","fb","fc","feml","ffut","fii","fivv",
           "fkor","flo","fl","fm","fmtb","fnw","fpec","fput","f","f+","fq",
           "ftfl","ftmp","ft","fut","fx","hput","ii","ivv","k3","k4","karsztb",
           "katl","katlv","kbor","kb","kc","keml","kfut","kii","kivv","kkor",
           "klhr", "klo","kl","km","kmtb","knw","kor","kpec","k","k+","kq",
           "ktfl","ktmp","kt","kx","l3","l4","latl","latlv","lbor","lb","lc",
           "ldu","leml","lfut","lii","livv","lkor","llo","ll","lm","lmtb","lnw",
           "lo","lpec","l","l+","lq","ls","ltfl","ltmp","lt","lx","mberc",
           "m","mtb","nw","p3","p4","palma","palp","patl","patlv","pbor",
           "pb","pc","pec","pek","peml","pfut","pii","pivv","pkor","plhr","plo",
           "pl","pmet","pm","pmtb","+","pnw","ppec","p","p+","pq","prst","pstm",
           "psziv","pszolo","ptfl","ptmp","pt","px","q","rc","refut","s3","s4",
           "salp","satl","satlv","sbarack","sbor","sb","sc","seml","sfut","sgy",
           "shor","sii","sivv","skor","slhr","slo","sl","sm","smtb","smz","snw",
           "spec","s","s+","sq","sszolo","ste","stfl","stj","stm","stmp","st","sx",
           "sz","tfl","tmp","tny","torp+","t","vcv","x","z3","z4","zatl","zatlv",
           "zbic","zbor","zb","zc","zeml","zfut","zii","zivv","zkor","zlhr","zlo",
           "zl","zkroki","zm","zmtb","znw","zpec","z","z+","zq","zszolo","zsziv",
           "ztfl","ztmp","zt","zut","zuveg","zx"
           ]

    for symbol in JEL:
        testsymbols.append(('LOC', '', { 'jel' : symbol, 'ref' : 'yy'}))

    for bg in OSMC_BACKGROUNDS:
        for fg in OSMC_FOREGROUNDS:
            testsymbols.append(('LOC', '', { 'osmc:symbol' : f"white:green{bg}:black{fg}"}))
            testsymbols.append(('LOC', '', { 'osmc:symbol' : f"red:red{bg}:green{fg}:A:black"}))
            testsymbols.append(('LOC', '', { 'osmc:symbol' : f"red:white{bg}:black{fg}"}))

#    testsymbols = [('LOC', '', {'osmc:symbol': 'red:red:green_diamond_left:A:black'})]

    with open(os.path.join(outdir, 'index.html'), 'w') as fd:
        fd.write("""
            <html><body bgcolor="#eee">
              <table><tr><th>Symbol</th><th>Tags</th></tr>
        """)


        for level, region, tags in testsymbols:
            sym = factory.create(tags, region, style=level)
            if sym is None:
                print("Unknown tags:", tags)
                continue

            sym.to_file(os.path.join(outdir, sym.uuid() + '.svg'), format='svg')

            fd.write(f'<tr><td><img src="{sym.uuid()}.svg" /></td><td><tt>{tags}</tt></td></tr>')



        fd.write("</table></body></html>")
