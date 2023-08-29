# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2023 Stéphane Chatty
# 

import sys
from urllib.parse import urlparse, quote as urlquote

import hashlib
import re

import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import os

from ..common.tags import Tags
from ..common.config import ShieldConfig
from ..common.shield_maker import ShieldMaker

class WikiSymbol(ShieldMaker):
    """ A shield with an SVG image located in the OSM wiki.
    """

    def __init__(self, uuid, url, config):
        self.uuid_pattern = uuid
        self.url = url
        self.config = config

    def render(self, ctx, w, h):
        data = self.find_resource('', self.url)
        rhdl = Rsvg.Handle.new_from_data(data)
        dim = rhdl.get_dimensions()

        ctx.scale(w/dim.width, h/dim.height)
        rhdl.render_cairo(ctx)


def create_for(tags: Tags, region: str, config: ShieldConfig):
    wiki_symbol = tags.get('wiki:symbol')
    if not (wiki_symbol):
        return None

    print(f'wiki:symbol = {wiki_symbol}', file=sys.stderr)
    if(urlparse(wiki_symbol).netloc):
        print(f'URLs are not accepted in tag wiki:symbol: {wiki_symbol}', file=sys.stderr)
        return None

    match_svg = re.search('(.*)\.svg$',  wiki_symbol)
    if not (match_svg):
        print(f'only SVG files are handled in tag wiki:symbol: {wiki_symbol}', file=sys.stderr)
        return None

    md5 = hashlib.md5(wiki_symbol.encode('utf-8')).hexdigest()
    c1 = md5[0]
    c2 = md5[1]
    filebasename = match_svg.group(1)
    filename =  urlquote(wiki_symbol.encode('utf-8'))
    url = f'https://wiki.openstreetmap.org/w/images/{c1}/{c1}{c2}/{filename}'
    print(f'     {url}', file=sys.stderr)
    return WikiSymbol(f'wiki_{filebasename}', url, config)

