# -*- coding: utf-8 -*-
'''
dtime: simple wrapper around datetime and time to ... well, make life easier ;-)
'''

from dtime import _dtime as dtime

dtime.__name__ = __name__
dtime.__package__ = __name__
dtime.__path__ = __path__

import sys
sys.modules[__name__] = dtime