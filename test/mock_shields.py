# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of the Waymarked Trails Map Project
# Copyright (C) 2011-2020 Sarah Hoffmann

from wmt_shields.common.tags import Tags
from wmt_shields.common.config import ShieldConfig

def NullShield(object):
    pass

def create_for(tags: Tags, region: str, config: ShieldConfig):
    return RefSymbol(ref, config)
