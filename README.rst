=======
Vncdesk
=======

*Vncdesk* was originally developed for scaling up applications on high DPI
screens. Applications run in VNC desktops.


Installation
============

Install dependencies:

* Python 3

* TigerVNC_ 1.4 or a compatible VNC server

* gtk-vnc_ 0.5 or compatible

Run with sufficient permissions::

  python setup.py install


Configuration
=============

Configuration for each desktop goes into a numbered directory below
``~/.vncdesk``. For example the configuration in ``~/.vncdesk/2/`` can be run
with::

  vncdesk 2

Files:

* ``settings.ini``, by example::

    [desktop]
    width = 1024
    height = 768

    [window]
    name = myxfig
    title = xfig in vncdesk
    class = FigInVncdesk
    scale_factor = 2

  The ``window`` section may be omitted.

  Consider that GDK 3 will also scale the VNC viewer via the environment
  variable ``GDK_SCALE``. You may want to disable GDK scaling in case you run
  into display errors.

* ``startup``: Startup script. Environment variables provided:

  - ``WIDTH``, ``HEIGHT``: Desktop size.

  - ``DISPLAY``: Display of the VNC server.

  - ``GUEST_DISPLAY``: Display of the VNC client.

  Example::

    #!/bin/sh
    xrdb -merge Xresources
    exec xfig -geometry ${WIDTH}x$HEIGHT+0+0

* Application specific files, for example ``Xresources``::

    xfig*image_editor: DISPLAY=$GUEST_DISPLAY xdg-open
    xfig*pdfviewer: DISPLAY=$GUEST_DISPLAY xdg-open
    xfig*browser: DISPLAY=$GUEST_DISPLAY xdg-open

* ``.password``: Generated every time anew, to password protect the connection
  also from other users on the same system.


Releasing a new version
=======================

* Use versioning scheme: `major.minor.patch`_

* Tag version in Git.


Coding convertions
==================

* Maximum line length: 80 characters

* Comments in reStructuredText.


License
=======

Except where noted otherwise, files are licensed under the WTFPL.

Copyright © 2015 `Felix E. Klee <mailto:felix.klee@inka.de>`

This work is free. You can redistribute it and/or modify it under the terms of
the Do What The Fuck You Want To Public License, Version 2, as published by Sam
Hocevar. See the COPYING file for more details.


.. _TigerVNC: http://tigervnc.org/
.. _major.minor.patch: http://semver.org/
.. _gtk-vnc: https://wiki.gnome.org/Projects/gtk-vnc
