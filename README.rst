============
Hangar Clock
============

Copyright (c) 2020 Phil Birkelbach

    .. image:: hclock.png

This is a simple PyQt application that turns a computer and display into a
clock that is useful around aviation.  It displays the time in local time,
the time in GMT, the date and a series of surface observations (METARs).

I'm currently using this on a Raspberry Pi and an LCD monitor in my hangar.
It seems to work well enough but it keeps crashing.  It seems to happen when
the internet availability is less than 100%.

Installation
------------

You'll need Python 3 and PyQt5 to run this little script.

Just download the hclock.py file, set it to executable and run it.

If you want the 7-segment display font then you'll need to download...
"DSEG7 Classic Mini" from https://www.soccercoin.eu/assets/fonts/fonts-DSEG_v045/DSEG7-Classic-MINI/
