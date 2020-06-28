#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# This file is part of the Waymarkedtrails Project
# Copyright (C) 2020 Sarah Hoffmann

from setuptools import setup

with open('README.md', 'r') as descfile:
    long_description = descfile.read()


setup(name='waymarkedtrails-shields',
      description='Library for generating SVG shields for the Waymarkedtrail project.',
      long_description=long_description,
      version='0.1',
      maintainer='Sarah Hoffmann',
      maintainer_email='lonvia@denofr.de',
      url='https://github.com/waymarkedtrails/waymarkedtrails-shields',
      license='GPL v3',
      packages=['wmt_shields',
                'wmt_shields.common',
                'wmt_shields.styles'
               ],
      package_data = { 'wmt_shields' : [ 'data/jel/**', 'data/kct/**', 'data/osmc/**', 'data/shields/**' ] },
      python_requires = ">=3.6",
      )
