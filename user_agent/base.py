# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
This module is for generating random, valid web navigator's
    configs & User-Agent HTTP headers.

Functions:
* generate_user_agent: generates User-Agent HTTP header
* generate_navigator:  generates web navigator's config
* generate_navigator_js:  generates web navigator's config with keys
    identical keys used in navigator object

FIXME:
* add Edge, Safari and Opera support
* add random config i.e. windows is more common than linux

Specs:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox
* http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
* https://developer.chrome.com/multidevice/user-agent
* http://www.javascriptkit.com/javatutors/navigator.shtml

Release history:
* https://en.wikipedia.org/wiki/Firefox_release_history
* https://en.wikipedia.org/wiki/Google_Chrome_release_history
* https://en.wikipedia.org/wiki/Internet_Explorer_version_history
* https://en.wikipedia.org/wiki/Android_version_history

Lists of user agents:
* http://www.useragentstring.com/
* http://www.user-agents.org/
* http://www.webapps-online.com/online-tools/user-agent-strings

"""
# pylint: enable=line-too-long

from random import choice, randint
from datetime import datetime, timedelta
from itertools import product

import six

from .warning import warn

# pylint: disable=unused-import
from .device import SMARTPHONE_DEV_IDS, TABLET_DEV_IDS

# pylint: enable=unused-import
from .error import InvalidOption

__all__ = ["generate_user_agent", "generate_navigator", "generate_navigator_js"]


DEVICE_TYPE_OS = {
    "desktop": ("win", "mac", "linux"),
    "smartphone": ("android",),
    "tablet": ("android",),
}
OS_DEVICE_TYPE = {
    "win": ("desktop",),
    "linux": ("desktop",),
    "mac": ("desktop",),
    "android": ("smartphone", "tablet"),
}
DEVICE_TYPE_NAVIGATOR = {
    "desktop": ("chrome", "firefox", "ie"),
    "smartphone": ("firefox", "chrome"),
    "tablet": ("firefox", "chrome"),
}
NAVIGATOR_DEVICE_TYPE = {
    "ie": ("desktop",),
    "chrome": ("desktop", "smartphone", "tablet"),
    "firefox": ("desktop", "smartphone", "tablet"),
}
OS_PLATFORM = {
    "win": (
        "Windows NT 5.1",  # Windows XP
        "Windows NT 6.1",  # Windows 7
        "Windows NT 6.2",  # Windows 8
        "Windows NT 6.3",  # Windows 8.1
        "Windows NT 10.0",  # Windows 10
    ),
    "mac": (
        "Macintosh; Intel Mac OS X 10.8",
        "Macintosh; Intel Mac OS X 10.9",
        "Macintosh; Intel Mac OS X 10.10",
        "Macintosh; Intel Mac OS X 10.11",
        "Macintosh; Intel Mac OS X 10.12",
        "Macintosh; Intel Mac OS X 10.13",
        "Macintosh; Intel Mac OS X 10.14",
        "Macintosh; Intel Mac OS X 10.15",
    ),
    "linux": (
        "X11; Linux",
        "X11; Ubuntu; Linux",
    ),
    "android": (
        "Android 4.4",  # 2013-10-31
        "Android 4.4.1",  # 2013-12-05
        "Android 4.4.2",  # 2013-12-09
        "Android 4.4.3",  # 2014-06-02
        "Android 4.4.4",  # 2014-06-19
        "Android 5.0",  # 2014-11-12
        "Android 5.0.1",  # 2014-12-02
        "Android 5.0.2",  # 2014-12-19
        "Android 5.1",  # 2015-03-09
        "Android 5.1.1",  # 2015-04-21
        "Android 6.0",  # 2015-10-05
        "Android 6.0.1",  # 2015-12-07
        "Android 7.0",  # 2016-08-22
        "Android 7.1",  # 2016-10-04
        "Android 7.1.1",  # 2016-12-05
        "Android 7.1.2",  # 2016-12-05
        "Android 8.0",  #
        "Android 8.1",  #
        "Android 9",  #
        "Android 10",  #
        "Android 11",  #
    ),
}
OS_CPU = {
    "win": (
        "",  # 32bit
        "Win64; x64",  # 64bit
        "WOW64",  # 32bit process on 64bit system
    ),
    "linux": (
        "i686",  # 32bit
        "x86_64",  # 64bit
        "i686 on x86_64",  # 32bit process on 64bit system
    ),
    "mac": ("",),
    "android": (
        "armv7l",  # 32bit
        "armv8l",  # 64bit
    ),
}
OS_NAVIGATOR = {
    "win": ("chrome", "firefox", "ie"),
    "mac": ("firefox", "chrome"),
    "linux": ("chrome", "firefox"),
    "android": ("firefox", "chrome"),
}
NAVIGATOR_OS = {
    "chrome": ("win", "linux", "mac", "android"),
    "firefox": ("win", "linux", "mac", "android"),
    "ie": ("win",),
}
# from wiki
FIREFOX_VERSION = (
    ("0.9", datetime(2004, 6, 28)),
    ("0.9.3", datetime(2004, 8, 4)),
    ("0.10", datetime(2004, 9, 14)),
    ("0.10.1", datetime(2004, 9, 14)),
    ("1.0.1", datetime(2005, 2, 24)),
    ("1.0.2", datetime(2005, 3, 23)),
    ("1.0.3", datetime(2005, 4, 15)),
    ("1.0.4", datetime(2005, 5, 11)),
    ("1.0.5", datetime(2005, 7, 12)),
    ("1.0.6", datetime(2005, 7, 19)),
    ("1.0.7", datetime(2005, 9, 20)),
    ("1.0.8", datetime(2006, 4, 13)),
    ("1.5.0.1", datetime(2006, 2, 1)),
    ("1.5.0.2", datetime(2006, 4, 13)),
    ("1.5.0.3", datetime(2006, 5, 2)),
    ("1.5.0.4", datetime(2006, 6, 1)),
    ("1.5.0.5", datetime(2006, 7, 27)),
    ("1.5.0.6", datetime(2006, 8, 2)),
    ("1.5.0.7", datetime(2006, 9, 14)),
    ("1.5.0.8", datetime(2006, 11, 7)),
    ("1.5.0.9", datetime(2007, 3, 20)),
    ("2.0.0.1", datetime(2006, 12, 19)),
    ("2.0.0.2", datetime(2007, 2, 23)),
    ("2.0.0.3", datetime(2007, 3, 20)),
    ("2.0.0.4", datetime(2007, 5, 30)),
    ("2.0.0.5", datetime(2007, 7, 17)),
    ("2.0.0.6", datetime(2007, 7, 30)),
    ("2.0.0.7", datetime(2007, 9, 18)),
    ("2.0.0.8", datetime(2007, 10, 18)),
    ("2.0.0.9", datetime(2007, 11, 1)),
    ("2.0.0.11", datetime(2007, 11, 30)),
    ("2.0.0.12", datetime(2008, 2, 7)),
    ("2.0.0.13", datetime(2008, 3, 25)),
    ("2.0.0.14", datetime(2008, 4, 16)),
    ("2.0.0.15", datetime(2008, 7, 1)),
    ("2.0.0.16", datetime(2008, 7, 15)),
    ("2.0.0.17", datetime(2008, 9, 23)),
    ("2.0.0.18", datetime(2008, 11, 12)),
    ("2.0.0.19", datetime(2008, 12, 16)),
    ("3.0.1", datetime(2008, 7, 16)),
    ("3.0.2", datetime(2008, 9, 23)),
    ("3.0.3", datetime(2008, 9, 26)),
    ("3.0.4", datetime(2008, 11, 12)),
    ("3.0.5", datetime(2008, 12, 16)),
    ("3.0.6", datetime(2009, 2, 3)),
    ("3.0.7", datetime(2009, 3, 4)),
    ("3.0.8", datetime(2009, 3, 27)),
    ("3.0.9", datetime(2009, 4, 21)),
    ("3.0.10", datetime(2009, 4, 27)),
    ("3.0.11", datetime(2009, 6, 11)),
    ("3.0.12", datetime(2009, 7, 21)),
    ("3.0.13", datetime(2009, 8, 3)),
    ("3.0.14", datetime(2009, 9, 9)),
    ("3.0.15", datetime(2009, 10, 27)),
    ("3.0.16", datetime(2009, 12, 15)),
    ("3.0.17", datetime(2010, 1, 5)),
    ("3.0.18", datetime(2010, 2, 17)),
    ("3.0.19", datetime(2010, 3, 30)),
    ("3.5.1", datetime(2009, 7, 16)),
    ("3.5.2", datetime(2009, 8, 3)),
    ("3.5.3", datetime(2009, 9, 9)),
    ("3.5.4", datetime(2009, 10, 27)),
    ("3.5.5", datetime(2009, 11, 5)),
    ("3.5.6", datetime(2009, 12, 15)),
    ("3.5.7", datetime(2010, 1, 5)),
    ("3.5.8", datetime(2010, 2, 17)),
    ("3.5.9", datetime(2010, 3, 30)),
    ("3.5.10", datetime(2010, 6, 22)),
    ("3.5.11", datetime(2010, 7, 20)),
    ("3.5.12", datetime(2010, 9, 7)),
    ("3.5.13", datetime(2010, 9, 15)),
    ("3.5.14", datetime(2010, 10, 19)),
    ("3.5.15", datetime(2010, 10, 27)),
    ("3.5.16", datetime(2010, 12, 9)),
    ("3.5.17", datetime(2011, 3, 1)),
    ("3.5.18", datetime(2011, 3, 22)),
    ("3.6.2", datetime(2010, 3, 22)),
    ("3.6.3", datetime(2010, 4, 1)),
    ("3.6.4", datetime(2010, 6, 22)),
    ("3.6.6", datetime(2010, 6, 26)),
    ("3.6.7", datetime(2010, 7, 20)),
    ("3.6.8", datetime(2010, 7, 23)),
    ("3.6.9", datetime(2010, 9, 7)),
    ("3.6.10", datetime(2010, 9, 15)),
    ("3.6.11", datetime(2010, 10, 19)),
    ("3.6.12", datetime(2010, 10, 27)),
    ("3.6.13", datetime(2010, 12, 9)),
    ("3.6.14", datetime(2011, 3, 1)),
    ("3.6.15", datetime(2011, 3, 4)),
    ("3.6.16", datetime(2011, 3, 22)),
    ("3.6.17", datetime(2011, 4, 28)),
    ("3.6.18", datetime(2011, 6, 21)),
    ("3.6.19", datetime(2011, 7, 11)),
    ("3.6.20", datetime(2011, 8, 16)),
    ("3.6.21", datetime(2011, 8, 30)),
    ("3.6.22", datetime(2011, 9, 6)),
    ("3.6.23", datetime(2011, 9, 27)),
    ("3.6.24", datetime(2011, 11, 8)),
    ("3.6.25", datetime(2011, 12, 20)),
    ("3.6.26", datetime(2012, 1, 31)),
    ("3.6.27", datetime(2012, 2, 17)),
    ("4.0", datetime(2011, 3, 22)),
    ("4.0.1", datetime(2011, 4, 28)),
    ("5.0", datetime(2011, 6, 21)),
    ("7.0", datetime(2011, 9, 27)),
    ("8.0", datetime(2011, 11, 8)),
    ("9.0", datetime(2011, 12, 20)),
    ("5.0.1", datetime(2011, 7, 11)),
    ("6.0", datetime(2011, 8, 16)),
    ("6.0.1", datetime(2011, 8, 30)),
    ("6.0.2", datetime(2011, 9, 6)),
    ("7.0.1", datetime(2011, 9, 29)),
    ("8.0.1", datetime(2011, 11, 21)),
    ("9.0.1", datetime(2011, 12, 21)),
    ("10.0", datetime(2012, 1, 31)),
    ("11.0", datetime(2012, 3, 13)),
    ("14.0.1", datetime(2012, 7, 17)),
    ("10.0.1", datetime(2012, 2, 10)),
    ("10.0.2", datetime(2012, 2, 16)),
    ("10.0.3", datetime(2012, 3, 13)),
    ("10.0.4", datetime(2012, 4, 24)),
    ("10.0.5", datetime(2012, 6, 5)),
    ("10.0.6", datetime(2012, 7, 17)),
    ("10.0.7", datetime(2012, 8, 28)),
    ("10.0.8", datetime(2012, 10, 9)),
    ("10.0.9", datetime(2012, 10, 12)),
    ("10.0.10", datetime(2012, 10, 26)),
    ("10.0.11", datetime(2012, 11, 20)),
    ("12.0", datetime(2012, 4, 24)),
    ("13.0", datetime(2012, 6, 5)),
    ("13.0.1", datetime(2012, 6, 15)),
    ("15.0", datetime(2012, 8, 28)),
    ("15.0.1", datetime(2012, 9, 6)),
    ("16.0", datetime(2012, 10, 9)),
    ("16.0.1", datetime(2012, 10, 11)),
    ("16.0.2", datetime(2012, 10, 26)),
    ("17.0", datetime(2012, 11, 20)),
    ("17.0.1", datetime(2012, 11, 30)),
    ("17.0.2", datetime(2013, 1, 8)),
    ("17.0.3", datetime(2013, 2, 19)),
    ("17.0.4", datetime(2013, 3, 7)),
    ("17.0.5", datetime(2013, 4, 2)),
    ("17.0.6", datetime(2013, 5, 14)),
    ("17.0.7", datetime(2013, 6, 25)),
    ("17.0.8", datetime(2013, 8, 6)),
    ("17.0.9", datetime(2013, 9, 17)),
    ("17.0.10", datetime(2013, 10, 29)),
    ("17.0.11", datetime(2013, 11, 15)),
    ("18.0", datetime(2013, 1, 6)),
    ("18.0.1", datetime(2013, 1, 18)),
    ("18.0.2", datetime(2013, 2, 5)),
    ("19.0", datetime(2013, 2, 19)),
    ("19.0.1", datetime(2013, 2, 27)),
    ("19.0.2", datetime(2013, 3, 7)),
    ("20.0", datetime(2013, 4, 2)),
    ("20.0.1", datetime(2013, 4, 11)),
    ("21.0", datetime(2013, 5, 14)),
    ("22.0", datetime(2013, 6, 25)),
    ("23.0", datetime(2013, 8, 6)),
    ("23.0.1", datetime(2013, 8, 17)),
    ("24.0", datetime(2013, 9, 17)),
    ("24.1.0", datetime(2013, 10, 29)),
    ("24.1.1", datetime(2013, 11, 15)),
    ("24.2.0", datetime(2013, 12, 10)),
    ("24.3.0", datetime(2013, 12, 10)),
    ("24.4.0", datetime(2013, 12, 10)),
    ("24.5.0", datetime(2013, 12, 10)),
    ("24.6.0", datetime(2013, 12, 10)),
    ("24.7.0", datetime(2013, 12, 10)),
    ("24.8.0", datetime(2013, 12, 10)),
    ("24.8.1", datetime(2013, 12, 10)),
    ("25.0", datetime(2013, 10, 29)),
    ("25.0.1", datetime(2013, 11, 15)),
    ("26.0", datetime(2013, 12, 10)),
    ("27.0", datetime(2014, 2, 4)),
    ("27.0.1", datetime(2014, 2, 14)),
    ("28.0", datetime(2014, 3, 18)),
    ("29.0", datetime(2014, 4, 29)),
    ("29.0.1", datetime(2014, 5, 9)),
    ("30.0", datetime(2014, 6, 10)),
    ("31.0", datetime(2014, 7, 22)),
    ("31.1.0", datetime(2014, 9, 2)),
    ("31.1.1", datetime(2014, 9, 2)),
    ("31.2.0", datetime(2014, 10, 14)),
    ("31.3.0", datetime(2014, 12, 1)),
    ("31.4.0", datetime(2015, 1, 13)),
    ("31.5.0", datetime(2015, 2, 24)),
    ("31.5.3", datetime(2015, 3, 21)),
    ("31.6.0", datetime(2015, 3, 31)),
    ("31.7.0", datetime(2015, 5, 12)),
    ("31.8.0", datetime(2015, 7, 2)),
    ("32.0", datetime(2014, 9, 2)),
    ("32.0.1", datetime(2014, 9, 12)),
    ("32.0.2", datetime(2014, 9, 18)),
    ("32.0.3", datetime(2014, 9, 24)),
    ("33.0", datetime(2014, 10, 14)),
    ("33.0.1", datetime(2014, 10, 24)),
    ("33.0.2", datetime(2014, 10, 28)),
    ("33.0.3", datetime(2014, 11, 7)),
    ("33.1", datetime(2014, 11, 10)),
    ("33.1.1", datetime(2014, 11, 14)),
    ("34.0", datetime(2014, 12, 1)),
    ("34.0.5", datetime(2014, 12, 1)),
    ("35.0", datetime(2015, 1, 13)),
    ("35.0.1", datetime(2015, 1, 27)),
    ("36.0", datetime(2015, 2, 24)),
    ("36.0.1", datetime(2015, 3, 6)),
    ("36.0.2", datetime(2015, 3, 16)),
    ("36.0.3", datetime(2015, 3, 20)),
    ("36.0.4", datetime(2015, 3, 21)),
    ("37.0", datetime(2015, 3, 31)),
    ("37.0.1", datetime(2015, 4, 3)),
    ("37.0.2", datetime(2015, 4, 20)),
    ("38.0", datetime(2015, 5, 12)),
    ("38.0.1", datetime(2015, 5, 14)),
    ("38.1.0", datetime(2015, 7, 2)),
    ("38.1.1", datetime(2015, 8, 6)),
    ("38.2.0", datetime(2015, 8, 11)),
    ("38.2.1", datetime(2015, 8, 27)),
    ("38.3.0", datetime(2015, 9, 22)),
    ("38.4.0", datetime(2015, 11, 3)),
    ("38.5.0", datetime(2015, 12, 15)),
    ("38.5.1", datetime(2015, 12, 21)),
    ("38.5.2", datetime(2015, 12, 22)),
    ("38.6.0", datetime(2016, 1, 26)),
    ("38.6.1", datetime(2016, 2, 11)),
    ("38.7.0", datetime(2016, 3, 8)),
    ("38.7.1", datetime(2016, 3, 16)),
    ("38.8.0", datetime(2016, 4, 26)),
    ("38.0.5", datetime(2015, 6, 2)),
    ("39.0", datetime(2015, 7, 2)),
    ("39.0.3", datetime(2015, 8, 6)),
    ("40.0", datetime(2015, 8, 11)),
    ("40.0.2", datetime(2015, 8, 13)),
    ("40.0.3", datetime(2015, 8, 27)),
    ("41.0", datetime(2015, 9, 22)),
    ("41.0.1", datetime(2015, 9, 30)),
    ("41.0.2", datetime(2015, 10, 15)),
    ("42.0", datetime(2015, 11, 3)),
    ("43.0", datetime(2015, 12, 15)),
    ("43.0.1", datetime(2015, 12, 18)),
    ("43.0.2", datetime(2015, 12, 22)),
    ("43.0.3", datetime(2015, 12, 28)),
    ("43.0.4", datetime(2016, 1, 6)),
    ("44.0", datetime(2016, 1, 26)),
    ("44.0.1", datetime(2016, 2, 8)),
    ("44.0.2", datetime(2016, 2, 11)),
    ("45.0", datetime(2016, 3, 8)),
    ("45.0.1", datetime(2016, 3, 16)),
    ("45.0.2", datetime(2016, 4, 12)),
    ("45.1.0", datetime(2016, 4, 26)),
    ("45.1.1", datetime(2016, 5, 3)),
    ("45.2.0", datetime(2016, 6, 7)),
    ("45.3.0", datetime(2016, 8, 2)),
    ("45.4.0", datetime(2016, 9, 20)),
    ("45.5.0", datetime(2016, 11, 15)),
    ("45.5.1", datetime(2016, 11, 30)),
    ("45.6.0", datetime(2016, 12, 13)),
    ("45.7.0", datetime(2017, 1, 24)),
    ("45.8.0", datetime(2017, 3, 7)),
    ("45.9.0", datetime(2017, 4, 19)),
    ("46.0", datetime(2016, 4, 26)),
    ("46.0.1", datetime(2016, 5, 3)),
    ("47.0", datetime(2016, 6, 7)),
    ("47.0.1", datetime(2016, 6, 28)),
    ("48.0", datetime(2016, 8, 2)),
    ("48.0.1", datetime(2016, 8, 18)),
    ("48.0.2", datetime(2016, 8, 24)),
    ("49.0", datetime(2016, 8, 2)),
    ("49.0.1", datetime(2016, 9, 23)),
    ("50.0", datetime(2016, 11, 15)),
    ("50.0.1", datetime(2016, 11, 28)),
    ("50.0.2", datetime(2016, 11, 30)),
    ("51.0", datetime(2017, 1, 24)),
    ("51.0.1", datetime(2017, 1, 26)),
    ("52.0", datetime(2017, 3, 7)),
    ("52.1.0", datetime(2017, 4, 19)),
    ("52.1.1", datetime(2017, 5, 19)),
    ("52.1.2", datetime(2017, 5, 19)),
    ("52.2.0", datetime(2017, 6, 13)),
    ("52.2.1", datetime(2017, 6, 29)),
    ("52.3.0", datetime(2017, 8, 8)),
    ("52.4.0", datetime(2017, 9, 28)),
    ("52.4.1", datetime(2017, 10, 9)),
    ("52.5.0", datetime(2017, 12, 7)),
    ("52.5.3", datetime(2017, 12, 28)),
    ("52.6.0", datetime(2018, 1, 23)),
    ("52.7.0", datetime(2018, 3, 13)),
    ("52.7.1", datetime(2018, 3, 14)),
    ("52.7.2", datetime(2018, 3, 16)),
    ("52.7.3", datetime(2018, 3, 26)),
    ("52.7.4", datetime(2018, 4, 30)),
    ("52.8.0", datetime(2018, 5, 9)),
    ("52.8.1", datetime(2018, 6, 6)),
    ("52.9.0", datetime(2018, 6, 26)),
    ("53.0", datetime(2017, 4, 19)),
    ("53.0.2", datetime(2017, 5, 5)),
    ("53.0.3", datetime(2017, 5, 19)),
    ("54.0", datetime(2017, 6, 13)),
    ("54.0.1", datetime(2017, 6, 29)),
    ("55.0", datetime(2017, 8, 8)),
    ("55.0.1", datetime(2017, 8, 10)),
    ("55.0.2", datetime(2017, 8, 16)),
    ("55.0.3", datetime(2017, 8, 25)),
    ("56.0", datetime(2017, 9, 28)),
    ("56.0.1", datetime(2017, 10, 9)),
    ("56.0.2", datetime(2017, 10, 26)),
    ("57.0", datetime(2017, 11, 14)),
    ("57.0.1", datetime(2017, 11, 29)),
    ("57.0.2", datetime(2017, 12, 7)),
    ("57.0.3", datetime(2017, 12, 28)),
    ("57.0.4", datetime(2018, 1, 4)),
    ("58.0", datetime(2018, 1, 23)),
    ("58.0.1", datetime(2018, 1, 29)),
    ("58.0.2", datetime(2018, 2, 7)),
    ("59.0", datetime(2018, 3, 13)),
    ("59.0.1", datetime(2018, 3, 16)),
    ("59.0.2", datetime(2018, 3, 26)),
    ("59.0.3", datetime(2018, 4, 30)),
    ("60.0", datetime(2018, 5, 9)),
    ("60.0.1", datetime(2018, 5, 16)),
    ("60.0.2", datetime(2018, 6, 6)),
    ("60.1.0", datetime(2018, 6, 26)),
    ("60.2.0", datetime(2018, 9, 5)),
    ("60.2.1", datetime(2018, 9, 21)),
    ("60.2.2", datetime(2018, 10, 2)),
    ("60.3.0", datetime(2018, 10, 23)),
    ("60.4.0", datetime(2018, 12, 11)),
    ("60.5.0", datetime(2019, 1, 29)),
    ("60.5.1", datetime(2019, 2, 12)),
    ("60.5.2", datetime(2019, 2, 22)),
    ("60.6.0", datetime(2019, 3, 19)),
    ("60.6.1", datetime(2019, 3, 22)),
    ("60.6.2", datetime(2019, 5, 5)),
    ("60.6.3", datetime(2019, 5, 8)),
    ("60.7.0", datetime(2019, 5, 21)),
    ("60.7.1", datetime(2019, 6, 18)),
    ("60.7.2", datetime(2019, 6, 20)),
    ("60.8.0", datetime(2019, 7, 9)),
    ("60.9.0", datetime(2019, 9, 3)),
    ("61.0", datetime(2018, 6, 26)),
    ("61.0.1", datetime(2018, 7, 5)),
    ("61.0.2", datetime(2018, 8, 8)),
    ("62.0", datetime(2018, 9, 5)),
    ("62.0.1", datetime(2018, 9, 7)),
    ("62.0.2", datetime(2018, 9, 21)),
    ("62.0.3", datetime(2018, 10, 2)),
    ("63.0", datetime(2018, 10, 23)),
    ("63.0.1", datetime(2018, 10, 31)),
    ("63.0.2", datetime(2018, 11, 7)),
    ("63.0.3", datetime(2018, 11, 15)),
    ("64.0", datetime(2018, 12, 11)),
    ("64.0.1", datetime(2018, 12, 14)),
    ("64.0.2", datetime(2019, 1, 9)),
    ("65.0", datetime(2019, 1, 29)),
    ("65.0.1", datetime(2019, 2, 12)),
    ("65.0.2", datetime(2019, 2, 28)),
    ("66.0", datetime(2019, 3, 19)),
    ("66.0.1", datetime(2019, 3, 22)),
    ("66.0.2", datetime(2019, 3, 27)),
    ("66.0.3", datetime(2019, 4, 10)),
    ("66.0.4", datetime(2019, 5, 5)),
    ("66.0.5", datetime(2019, 5, 7)),
    ("67.0", datetime(2019, 5, 21)),
    ("67.0.1", datetime(2019, 6, 4)),
    ("67.0.2", datetime(2019, 6, 11)),
    ("67.0.3", datetime(2019, 6, 18)),
    ("67.0.4", datetime(2019, 6, 20)),
    ("68.0", datetime(2019, 7, 13)),
    ("68.0.1", datetime(2019, 7, 18)),
    ("68.0.2", datetime(2019, 8, 14)),
    ("68.1.0", datetime(2019, 9, 3)),
    ("68.2.0", datetime(2019, 10, 22)),
    ("68.3.0", datetime(2019, 12, 3)),
    ("68.4.0", datetime(2020, 1, 7)),
    ("68.4.1", datetime(2020, 1, 8)),
    ("68.4.2", datetime(2020, 1, 20)),
    ("68.5.0", datetime(2020, 2, 11)),
    ("68.6.0", datetime(2020, 3, 10)),
    ("68.6.1", datetime(2020, 4, 3)),
    ("68.7.0", datetime(2020, 4, 7)),
    ("68.8.0", datetime(2020, 5, 5)),
    ("68.9.0", datetime(2020, 6, 2)),
    ("68.10.0", datetime(2020, 6, 30)),
    ("68.11.0", datetime(2020, 7, 28)),
    ("68.12.0", datetime(2020, 8, 25)),
    ("69.0", datetime(2019, 9, 3)),
    ("69.0.1", datetime(2019, 9, 18)),
    ("69.0.2", datetime(2019, 10, 3)),
    ("69.0.3", datetime(2019, 10, 10)),
    ("70.0", datetime(2019, 10, 22)),
    ("70.0.1", datetime(2019, 10, 31)),
    ("71.0", datetime(2019, 12, 3)),
    ("72.0", datetime(2020, 1, 7)),
    ("72.0.1", datetime(2020, 1, 8)),
    ("72.0.2", datetime(2020, 1, 20)),
    ("73.0", datetime(2020, 2, 11)),
    ("73.0.1", datetime(2020, 2, 18)),
    ("74.0", datetime(2020, 3, 10)),
    ("74.0.1", datetime(2020, 4, 3)),
    ("75.0", datetime(2020, 4, 7)),
    ("76.0", datetime(2020, 5, 5)),
    ("76.0.1", datetime(2020, 5, 8)),
    ("77.0", datetime(2020, 6, 2)),
    ("77.0.1", datetime(2020, 6, 3)),
    ("78.0", datetime(2020, 6, 30)),
    ("78.0.1", datetime(2020, 7, 1)),
    ("78.0.2", datetime(2020, 7, 9)),
    ("78.1.0", datetime(2020, 7, 28)),
    ("78.2.0", datetime(2020, 8, 25)),
    ("78.3.0", datetime(2020, 9, 22)),
    ("78.3.1", datetime(2020, 10, 1)),
    ("78.4.0", datetime(2020, 10, 20)),
    ("78.4.1", datetime(2020, 11, 10)),
    ("78.5.0", datetime(2020, 11, 17)),
    ("78.6.0", datetime(2020, 12, 15)),
    ("78.6.1", datetime(2021, 1, 6)),
    ("79.0", datetime(2020, 7, 28)),
    ("80.0", datetime(2020, 8, 25)),
    ("80.0.1", datetime(2020, 9, 1)),
    ("81.0", datetime(2020, 9, 22)),
    ("81.0.1", datetime(2020, 10, 1)),
    ("81.0.2", datetime(2020, 10, 13)),
    ("82.0", datetime(2020, 10, 20)),
    ("82.0.1", datetime(2020, 10, 27)),
    ("82.0.2", datetime(2020, 10, 28)),
    ("82.0.3", datetime(2020, 11, 10)),
    ("83.0", datetime(2020, 11, 17)),
    ("84.0", datetime(2020, 12, 15)),
    ("84.0.1", datetime(2020, 12, 22)),
    ("84.0.2", datetime(2021, 1, 6)),
)
# from https://google_chrome.zh.downloadastro.com/old_versions/
CHROME_BUILD = (
    (49, 2623, 2623),  # 2016-07-04
    (50, 2661, 2661),  # 2016-16-05
    (51, 2704, 2704),  # 2016-24-06
    (52, 2743, 2743),  # 2016-04-08
    (53, 2785, 2785),  # 2016-10-09
    (54, 2840, 2840),  # 2016-10-11
    (55, 2883, 2883),  # 2017-11-01
    (56, 2924, 2924),  # 2017-02-02
    (57, 2987, 2987),  # 2017-30-03
    (58, 3029, 3029),  # 2017-18-05
    (59, 3071, 3071),  # 2017-18-07
    (60, 3112, 3112),  # 2017-14-09
    (61, 3163, 3163),  # 2017-07-10
    (62, 3202, 3202),  # 2017-14-11
    (63, 3239, 3239),  # 2018-05-01
    (64, 3251, 3282),  # 2017-28-10
    (65, 3325, 3325),  # 2018-23-03
    (66, 3359, 3359),  # 2018-18-05
    (67, 3396, 3396),  # 2018-27-06
    (68, 3440, 3440),  # 2018-10-08
    (69, 3497, 3497),  # 2018-21-09
    (70, 3538, 3538),  # 2018-21-11
    (71, 3578, 3578),  # 2018-14-12
    (72, 3626, 3626),  # 2019-01-03
    (73, 3683, 3683),  # 2019-05-04
    (74, 3729, 3729),  # 2019-23-05
    (75, 3770, 3770),  # 2019-18-07
    (76, 3809, 3809),  # 2019-06-09
    (77, 3865, 3865),  # 2019-11-10
    (78, 3904, 3904),  # 2019-21-11
    (79, 3945, 3945),  # 2020-18-01
    (80, 3987, 3987),  # 2020-03-04
    (81, 4044, 4044),  # 2020-07-05
    (83, 4103, 4103),  # 2020-26-06
    (84, 4147, 4147),  # 2020-21-08
    (85, 4183, 4183),  # 2020-23-09
    (86, 4240, 4240),  # 2020-13-11
    (87, 4280, 4280),  # 2021-10-01
)
IE_VERSION = (
    # (numeric ver, string ver, trident ver) # release year
    (8, "MSIE 8.0", "4.0"),  # 2009
    (9, "MSIE 9.0", "5.0"),  # 2011
    (10, "MSIE 10.0", "6.0"),  # 2012
    (11, "MSIE 11.0", "7.0"),  # 2013
)
USER_AGENT_TEMPLATE = {
    "firefox": (
        "Mozilla/5.0"
        " ({system[ua_platform]}; rv:{app[build_version]})"
        " Gecko/{app[geckotrail]}"
        " Firefox/{app[build_version]}"
    ),
    "chrome": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Safari/537.36"
    ),
    "chrome_smartphone": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Mobile Safari/537.36"
    ),
    "chrome_tablet": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Safari/537.36"
    ),
    "ie_less_11": (
        "Mozilla/5.0"
        " (compatible; {app[build_version]}; {system[ua_platform]};"
        " Trident/{app[trident_version]})"
    ),
    "ie_11": (
        "Mozilla/5.0"
        " ({system[ua_platform]}; Trident/{app[trident_version]};"
        " rv:11.0) like Gecko"
    ),
}


def get_firefox_build():
    build_ver, date_from = choice(FIREFOX_VERSION)
    try:
        idx = FIREFOX_VERSION.index((build_ver, date_from))
        _, date_to = FIREFOX_VERSION[idx + 1]
    except IndexError:
        date_to = date_from + timedelta(days=1)
    sec_range = (date_to - date_from).total_seconds() - 1
    build_rnd_time = date_from + timedelta(seconds=randint(0, max(sec_range, 100000)))
    return build_ver, build_rnd_time.strftime("%Y%m%d%H%M%S")


def get_chrome_build():
    build = choice(CHROME_BUILD)
    return "%d.0.%d.%d" % (
        build[0],
        randint(build[1], build[2]),
        randint(0, 120),
    )


def get_ie_build():
    """
    Return random IE version as tuple
    (numeric_version, us-string component)

    Example: (8, 'MSIE 8.0')
    """

    return choice(IE_VERSION)


MACOSX_CHROME_BUILD_RANGE = {
    # https://en.wikipedia.org/wiki/MacOS#Release_history
    "10.8": (0, 8),
    "10.9": (0, 5),
    "10.10": (0, 5),
    "10.11": (0, 6),
    "10.12": (0, 6),
    "10.13": (0, 6),
    "10.14": (0, 6),
    "10.15": (0, 7),
    "11.0": (0, 2),
}


def fix_chrome_mac_platform(platform):
    """
    Chrome on Mac OS adds minor version number and uses underscores instead
    of dots. E.g. platform for Firefox will be: 'Intel Mac OS X 10.11'
    but for Chrome it will be 'Intel Mac OS X 10_11_6'.

    :param platform: - string like "Macintosh; Intel Mac OS X 10.8"
    :return: platform with version number including minor number and formatted
    with underscores, e.g. "Macintosh; Intel Mac OS X 10_8_2"
    """
    ver = platform.split("OS X ")[1]
    build_range = range(*MACOSX_CHROME_BUILD_RANGE[ver])
    build = choice(build_range)
    mac_ver = ver.replace(".", "_") + "_" + str(build)
    return "Macintosh; Intel Mac OS X %s" % mac_ver


def build_system_components(device_type, os_id, navigator_id):
    """
    For given os_id build random platform and oscpu
    components

    Returns dict {platform_version, platform, ua_platform, oscpu}

    platform_version is OS name used in different places
    ua_platform goes to navigator.platform
    platform is used in building navigator.userAgent
    oscpu goes to navigator.oscpu
    """

    if os_id == "win":
        platform_version = choice(OS_PLATFORM["win"])
        cpu = choice(OS_CPU["win"])
        if cpu:
            platform = "%s; %s" % (platform_version, cpu)
        else:
            platform = platform_version
        res = {
            "platform_version": platform_version,
            "platform": platform,
            "ua_platform": platform,
            "oscpu": platform,
        }
    elif os_id == "linux":
        cpu = choice(OS_CPU["linux"])
        platform_version = choice(OS_PLATFORM["linux"])
        platform = "%s %s" % (platform_version, cpu)
        res = {
            "platform_version": platform_version,
            "platform": platform,
            "ua_platform": platform,
            "oscpu": "Linux %s" % cpu,
        }
    elif os_id == "mac":
        cpu = choice(OS_CPU["mac"])
        platform_version = choice(OS_PLATFORM["mac"])
        platform = platform_version
        if navigator_id == "chrome":
            platform = fix_chrome_mac_platform(platform)
        res = {
            "platform_version": platform_version,
            "platform": "MacIntel",
            "ua_platform": platform,
            "oscpu": "Intel Mac OS X %s" % platform.split(" ")[-1],
        }
    elif os_id == "android":
        assert navigator_id in ("firefox", "chrome")
        assert device_type in ("smartphone", "tablet")
        platform_version = choice(OS_PLATFORM["android"])
        if navigator_id == "firefox":
            if device_type == "smartphone":
                ua_platform = "%s; Mobile" % platform_version
            elif device_type == "tablet":
                ua_platform = "%s; Tablet" % platform_version
        elif navigator_id == "chrome":
            device_id = choice(SMARTPHONE_DEV_IDS)
            ua_platform = "Linux; %s; %s" % (platform_version, device_id)
        oscpu = "Linux %s" % choice(OS_CPU["android"])
        res = {
            "platform_version": platform_version,
            "ua_platform": ua_platform,
            "platform": oscpu,
            "oscpu": oscpu,
        }
    return res


def build_app_components(os_id, navigator_id):
    """
    For given navigator_id build app features

    Returns dict {name, product_sub, vendor, build_version, build_id}
    """

    if navigator_id == "firefox":
        build_version, build_id = get_firefox_build()
        if os_id in ("win", "linux", "mac"):
            geckotrail = "20100101"
        else:
            geckotrail = build_version
        res = {
            "name": "Netscape",
            "product_sub": "20100101",
            "vendor": "",
            "build_version": build_version,
            "build_id": build_id,
            "geckotrail": geckotrail,
        }
    elif navigator_id == "chrome":
        res = {
            "name": "Netscape",
            "product_sub": "20030107",
            "vendor": "Google Inc.",
            "build_version": get_chrome_build(),
            "build_id": None,
        }
    elif navigator_id == "ie":
        num_ver, build_version, trident_version = get_ie_build()
        if num_ver >= 11:
            app_name = "Netscape"
        else:
            app_name = "Microsoft Internet Explorer"
        res = {
            "name": app_name,
            "product_sub": None,
            "vendor": "",
            "build_version": build_version,
            "build_id": None,
            "trident_version": trident_version,
        }
    return res


def get_option_choices(opt_name, opt_value, default_value, all_choices):
    """
    Generate possible choices for the option `opt_name`
    limited to `opt_value` value with default value
    as `default_value`
    """

    choices = []
    if isinstance(opt_value, six.string_types):
        choices = [opt_value]
    elif isinstance(opt_value, (list, tuple)):
        choices = list(opt_value)
    elif opt_value is None:
        choices = default_value
    else:
        raise InvalidOption(
            "Option %s has invalid" " value: %s" % (opt_name, opt_value)
        )
    if "all" in choices:
        choices = all_choices
    for item in choices:
        if item not in all_choices:
            raise InvalidOption(
                "Choices of option %s contains invalid" " item: %s" % (opt_name, item)
            )
    return choices


def pick_config_ids(device_type, os, navigator):
    """
    Select one random pair (device_type, os_id, navigator_id) from
    all possible combinations matching the given os and
    navigator filters.

    :param os: allowed os(es)
    :type os: string or list/tuple or None
    :param navigator: allowed browser engine(s)
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    """

    if os is None:
        default_dev_types = ["desktop"]
    else:
        default_dev_types = list(DEVICE_TYPE_OS.keys())
    dev_type_choices = get_option_choices(
        "device_type", device_type, default_dev_types, list(DEVICE_TYPE_OS.keys())
    )
    os_choices = get_option_choices(
        "os", os, list(OS_NAVIGATOR.keys()), list(OS_NAVIGATOR.keys())
    )
    nav_choices = get_option_choices(
        "navigator", navigator, list(NAVIGATOR_OS.keys()), list(NAVIGATOR_OS.keys())
    )

    variants = []
    for dev, os, nav in product(dev_type_choices, os_choices, nav_choices):

        if (
            os in DEVICE_TYPE_OS[dev]
            and nav in DEVICE_TYPE_NAVIGATOR[dev]
            and nav in OS_NAVIGATOR[os]
        ):
            variants.append((dev, os, nav))
    if not variants:
        raise InvalidOption(
            "Options device_type, os and navigator" " conflicts with each other"
        )
    device_type, os_id, navigator_id = choice(variants)

    assert os_id in OS_PLATFORM
    assert navigator_id in NAVIGATOR_OS
    assert device_type in DEVICE_TYPE_OS

    return device_type, os_id, navigator_id


def choose_ua_template(device_type, navigator_id, app):
    tpl_name = navigator_id
    if navigator_id == "ie":
        tpl_name = "ie_11" if app["build_version"] == "MSIE 11.0" else "ie_less_11"
    if navigator_id == "chrome":
        if device_type == "smartphone":
            tpl_name = "chrome_smartphone"
        if device_type == "tablet":
            tpl_name = "chrome_tablet"
    return USER_AGENT_TEMPLATE[tpl_name]


def build_navigator_app_version(os_id, navigator_id, platform_version, user_agent):
    if navigator_id in ("chrome", "ie"):
        assert user_agent.startswith("Mozilla/")
        app_version = user_agent.split("Mozilla/", 1)[1]
    elif navigator_id == "firefox":
        if os_id == "android":
            app_version = "5.0 (%s)" % platform_version
        else:
            os_token = {
                "win": "Windows",
                "mac": "Macintosh",
                "linux": "X11",
            }[os_id]
            app_version = "5.0 (%s)" % os_token
    return app_version


def generate_navigator(os=None, navigator=None, platform=None, device_type=None):
    """
    Generates web navigator's config

    :param os: limit list of oses for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"

    :return: User-Agent config
    :rtype: dict with keys (os, name, platform, oscpu, build_version,
                            build_id, app_version, app_name, app_code_name,
                            product, product_sub, vendor, vendor_sub,
                            user_agent)
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed platforms and navigators
    :raise InvalidOption: if any of passed options is invalid
    """

    if platform is not None:
        os = platform
        warn(
            "The `platform` option is deprecated." " Use `os` option instead.",
            stacklevel=3,
        )
    device_type, os_id, navigator_id = pick_config_ids(device_type, os, navigator)
    system = build_system_components(device_type, os_id, navigator_id)
    app = build_app_components(os_id, navigator_id)
    ua_template = choose_ua_template(device_type, navigator_id, app)
    user_agent = ua_template.format(system=system, app=app)
    app_version = build_navigator_app_version(
        os_id, navigator_id, system["platform_version"], user_agent
    )
    return {
        # ids
        "os_id": os_id,
        "navigator_id": navigator_id,
        # system components
        "platform": system["platform"],
        "oscpu": system["oscpu"],
        # app components
        "build_version": app["build_version"],
        "build_id": app["build_id"],
        "app_version": app_version,
        "app_name": app["name"],
        "app_code_name": "Mozilla",
        "product": "Gecko",
        "product_sub": app["product_sub"],
        "vendor": app["vendor"],
        "vendor_sub": "",
        # compiled user agent
        "user_agent": user_agent,
    }


def generate_user_agent(os=None, navigator=None, platform=None, device_type=None):
    """
    Generates HTTP User-Agent header

    :param os: limit list of os for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    :return: User-Agent string
    :rtype: string
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed oses and navigators
    :raise InvalidOption: if any of passed options is invalid
    """
    return generate_navigator(
        os=os, navigator=navigator, platform=platform, device_type=device_type
    )["user_agent"]


def generate_navigator_js(os=None, navigator=None, platform=None, device_type=None):
    """
    Generates web navigator's config with keys corresponding
    to keys of `windows.navigator` JavaScript object.

    :param os: limit list of oses for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    :return: User-Agent config
    :rtype: dict with keys (TODO)
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed oses and navigators
    :raise InvalidOption: if any of passed options is invalid
    """

    config = generate_navigator(
        os=os, navigator=navigator, platform=platform, device_type=device_type
    )
    return {
        "appCodeName": config["app_code_name"],
        "appName": config["app_name"],
        "appVersion": config["app_version"],
        "platform": config["platform"],
        "userAgent": config["user_agent"],
        "oscpu": config["oscpu"],
        "product": config["product"],
        "productSub": config["product_sub"],
        "vendor": config["vendor"],
        "vendorSub": config["vendor_sub"],
        "buildID": config["build_id"],
    }
