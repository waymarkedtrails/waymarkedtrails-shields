# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

class WmtConfig(object):
    """ Default configuration as used by the waymarkedtrails project.
    """
    data_dir = "{data}"

    image_height = 15
    image_width = 15
    image_border_width = 2.5

    text_border_width = 2.5
    text_bgcolor = (1, 1, 1) # white
    text_color = (0, 0, 0) # black
    text_font = "DejaVu-Sans Condensed Bold 7.5"

    swiss_mobile_font ='DejaVu-Sans Oblique Bold 10'
    swiss_mobile_bgcolor = (0.48, 0.66, 0.0)
    swiss_mobile_color = (1, 1, 1)
    swiss_mobile_networks = ('rwn', 'nwn', 'lwn')
    swiss_mobile_operators = ('swiss mobility',
                              'wanderland schweiz', 
                              'schweiz mobil',
                              'skatingland schweiz',
                              'la suisse à pied,
                              'veloland schweiz',
                              'mountainbikeland schweiz',
                              'schweizmobil',
                              'stiftung schweizmobil'
                             )

    jel_path = "jel"
    jel_types = ("3","4","atl","atlv","bfk","bor","b","but","c","eml","f3","f4",
                 "fatl","fatlv","fbor","fb","fc","feml","ffut","fii","fivv",
                 "fkor","flo","fl","fm","fmtb","fnw","fpec","f","f+","fq","ftfl",
                 "ftmp","ft","fut","fx","ii","ivv","k3","k4","karsztb","katl",
                 "katlv","kbor","kb","kc","keml","kfut","kii","kivv","kkor",
                 "klo","kl","km","kmtb","knw","kor","kpec","k","k+","kq","ktfl",
                 "ktmp","kt","kx","l3","l4","latl","latlv","lbor","lb","lc",
                 "leml","lfut","lii","livv","lkor","llo","ll","lm","lmtb","lnw",
                 "lo","lpec","l","l+","lq","ls","ltfl","ltmp","lt","lx","mberc",
                 "m","mtb","nw","p3","p4","palma","palp","patl","patlv","pbor",
                 "pb","pc","pec","peml","pfut","pii","pivv","pkor","plo","pl",
                 "pmet","pm","pmtb","+","pnw","ppec","p","p+","pq","ptfl","ptmp",
                 "pt","px","q","rc","s3","s4","salp","satl","satlv","sbarack",
                 "sbor","sb","sc","seml","sfut","sgy","sii","sivv","skor","slo",
                 "sl","sm","smtb","smz","snw","spec","s","s+","sq","ste","stfl",
                 "stj","stm","stmp","st","sx","sz","tfl","tmp","tny","t","x",
                 "z3","z4","zatl","zatlv","zbic","zbor","zb","zc","zeml","zfut",
                 "zii","zivv","zkor","zlo","zl","zm","zmtb","znw","zpec","z",
                 "z+","zq","ztfl","ztmp","zt","zut","zx","zszolo")

    cai_border_width = 5
    kct_path = 'kct'
    kct_colors = {'red' : (1, 0, 0),
                  'blue' : (0.04, 0.34, 0.64),
                  'green' : (0, 0.51, 0.31),
                  'yellow' : (1.0, 0.81, 0)}
    kct_types = ('major', 'local', 'interesting_object', 'learning',
                 'peak', 'ruin', 'spring', 'horse')

    osmc_path = 'osmc'
    osmc_colors = { 'black' : (0, 0, 0),
                    'blue' : (0.03, 0.20, 1),
                    'brown' : (0.59, 0.32, 0.11),
                    'gray' : (0.5, 0.5, 0.5),
                    'green' : (0.34, 0.68, 0),
                    'orange' : (1, 0.64, 0.02),
                    'purple' : (0.70, 0.06, 0.74),
                    'red' : (0.88, 0.15, 0.05),
                    'white' : (1, 1, 1),
                    'yellow' : (0.91, 0.88, 0.16)
                  }

    shield_path = 'shields'
    shield_names = {}

    slope_colors = ((0, 0, 0),
                    (0.0, 0.439, 0.16),
                    (0.082, 0.18, 0.925),
                    (0.698, 0.012, 0.012),
                    (0, 0, 0),
                    (0, 0, 0),
                    (0, 0, 0),
                    (1.0, 0.639, 0.016))

    # used in backgrounds
    color_names = {
               'black'   : (0., 0., 0.),
               'gray'    : (.5, .5, .5),
               'grey'    : (.5, .5, .5),
               'maroon'  : (.5, 0., 0.),
               'olive'   : (.5, .5, 0.),
               'green'   : (0., .5, 0.),
               'teal'    : (0., .5, .5),
               'navy'    : (0., 0., .5),
               'purple'  : (.5, 0., .5),
               'white'   : (1., 1., 1.),
               'silver'  : (.75, .75, .75),
               'red'     : (1., 0., 0.),
               'yellow'  : (1., 1., 0.),
               'lime'    : (0., 1., 0.),
               'aqua'    : (0., 1., 1.),
               'blue'    : (0., 0., 1.),
               'fuchsia' : (1., 0., 1.) }

    # used for underlining text
    colorbox_names = {
               'aqua'    : [(0., 1., 1.), (.5, .5, .5)],
               'black'   : [(0., 0., 0.), (1., 1., 1.)],
               'blue'    : [(0., 0., 1.), (1., 1., 1.)],
               'brown'   : [(0.76, 0.63, 0.08), (.3, .3, .3)],
               'green'   : [(0., 1., 0.), (.5, .5, .5)],
               'gray'    : [(.5, .5, .5), (1., 1., 1.)],
               'grey'    : [(.6, .6, .6), (.6, .6, .6)],
               'maroon'  : [(.5, 0., 0.), (1., 1., 1.)],
               'orange'  : [(1., .65, 0.), (1., 1., 1.)],
               'pink'    : [(1., 0., 1.), (1., 1., 1.)],
               'purple'  : [(.5, 0., .5), (1., 1., 1.)],
               'red'     : [(1., 0., 0.), (1., 1., 1.)],
               'violet'  : [(.55, .22, .79), (1., 1., 1.)],
               'white'   : [(1., 1., 1.), (0., 0., 0.)],
               'yellow'  : [(1., 1., 0.), (.51, .48, .23)],
               }

    # settings for different levels of network
    style_config = {
        "INT" : {
            'border_color' : (0.7, 0.01, 0.01),
        },
        "NAT" : {
            'border_color' : (0.08, 0.18, 0.92),
        },
        "LOC" : {
            'border_color' : (0.55, 0.0, 0.86),
        },
        "REG" : {
            'border_color' : (0.99, 0.64, 0.02),
        }
    }
