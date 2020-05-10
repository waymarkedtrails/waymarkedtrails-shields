This package contains the library used for creating SVG shields for the
Waymarkedtrails project.

Requirements
------------

At least Python 3.6 is needed. Further requirements are Cairo, Pango
and Rsvg with their respective Python bindings via the Gobject inspector.

On Debian the requirements can be installed with:

    sudo apt install python3-gi python3-gi-cairo libcairo2-dev\
             gir1.2-pango-1.0 gir1.2-rsvg-2.0


Installation
------------

Simply install with setup tools:

    ./setup.py install

Usage
-----

For usage please have a look at `test/render_test.py`.

Copyright
---------

The source code is available under GPL. See COPYING for more information.

