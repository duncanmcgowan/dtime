# -*- coding: utf-8 -*-
'''
Really simple date/time utilities to make life easy.

- get current/any time, return dict of useful stuff
- simple date/time formatting
- basic time operations
- simple conversion to/from Python datetime object

The returned JSON-like dictionary object is intended to assist
in web apps, avoiding the need to mess around with datetime strings.

(C) Duncan McGowan 2016
'''

import time as pytime
from datetime import datetime as pydatetime
import re

_timer_time = { 'start_time': None, 'end_time': None, 'delta_time': None }

_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_MONTHS = ("January",
           "February",
           "March",
           "April",
           "May",
           "June",
           "July",
           "August",
           "September",
           "October",
           "November",
           "December")

_dtmap = {'year'        : 0, 
          'month'       : 1,
          'day'         : 2,
          'hour'        : 3,
          'minute'      : 4,
          'second'      : 5,
          'microsecond' : 6,
          'timezone'    : 7 }



class _dtime(object):
   
   OBJECT_NAME = "dtime"
   
   def __str__(self):
      '''
      Return a string in format: YYYY-MM-DD HH:MM:SS.uuuuuu, being the
      same format as str(datetime_object)
      
      eg; import dtime; dt = dtime(); str(dt)
      '''
      dt_s = "%d-%02d-%02d %02d:%02d:%02d.%d" % (
         self.datetime['year'],
         self.datetime['month'],
         self.datetime['day'],
         self.datetime['hour'],
         self.datetime['minute'],
         self.datetime['second'],
         self.datetime['microsecond'] )
      return dt_s
   
   
   def __init__(self, arg=None):
      '''
      Constructor.
      If arg (not using **kwargs as might not be a mapping) is a python datetime object, use that.
      If it is a dictionary of date/time kv pairs, use that.
      If it is an integer, assume it is a timestamp and use that.
      If it is a string, assume it is ISO or similar and try to use that (!).
      Otherwise do nothing :-)
      '''
      self.datetime = {
         'year'         : 0,
         'month'        : 0,
         'day'          : 0,
         'hour'         : 0,
         'minute'       : 0,
         'second'       : 0,
         'microsecond'  : 0,
         'timestamp'    : 0,
         'utctimestamp' : 0,
         'timezone'     : None,
         'day_of_week'  : None,
         'month_str'    : None }
      
      self.start_time = self.end_time = self.delta_time = 0
      
      if type(arg) is pydatetime:
         
         ''' Initialise from datetime object '''
         
         self._fromdatetime(arg)
         
      elif type(arg) is str:
         
         ''' Initialise from string in format: YYY-MM-DD HH:MM:SS.ss (or similar) '''
         
         self._fromstring(arg)
         
      elif type(arg) is int:
         
         ''' Initialise from timestamp '''
         
         self._fromtimestamp(arg)
         
      elif type(arg) is dict:
         
         ''' Initialise from user-defined dict '''
         
         self._fromdatetime(self.todatetime(arg))
         
      else:
         
         ''' Initialise from current time '''
         
         self._fromdatetime(pydatetime.now())
         
      self.datetime['timestamp'] = self.totimestamp(self.datetime)
      self.datetime['utctimestamp'] = self.totimestamp(self.datetime, utc=True)
               
   
   def _fromstring(self, arg):
      ''' 
      Convert from a string (this is the ugly bit)
      Should be something like;
      YYYY-MM-DD HH:MM:SS.ss
      YYYY-MM-DD HH:MM:SSZ
      YYYY-MM-DDTHH:MM:SS.SSZ 
      '''
      
      if len(arg) < 19:
         raise ValueError("Invalid string: use YYYY-MM-DD HH:MM:SS at least!")
      
      mat = re.match("\d{4}[-]\d{2}[-]\d{2}[ T]\d{2}[:]\d{2}[:]\d{2}",arg)
      if not bool(mat):
         raise ValueError("Invalid date/time format: use YYYY-MM-DD HH:MM:SS or similar")
      
      try:
         self.datetime['year']   = int(arg[0:4])
         self.datetime['month']  = int(arg[5:7])
         self.datetime['day']    = int(arg[8:10])
         self.datetime['hour']   = int(arg[11:13])
         self.datetime['minute'] = int(arg[14:16])
         self.datetime['second'] = int(arg[17:19])
         if len(arg) > 19 and arg.find(".") > -1:
            usecs = arg[arg.find(".")+1:]
            if usecs.find("Z") > -1:
               usecs = usecs[:-1]
            self.datetime['microsecond'] = int(usecs)
         self._fromdatetime(self.todatetime(self.datetime))
      except Exception as exp:
         raise ValueError("Unable to convert string (%s)" % str(exp))
      
         
   def _fromdatetime(self, dt):
      ''' Convert from a datetime object '''
      self.datetime['year']         = dt.year
      self.datetime['month']        = dt.month # 1-12
      self.datetime['day']          = dt.day # 1-31
      self.datetime['day_of_week']  = _DAYS[dt.weekday()]
      self.datetime['month_str']    = _MONTHS[dt.month-1]
      self.datetime['hour']         = dt.hour
      self.datetime['minute']       = dt.minute
      self.datetime['second']       = dt.second
      self.datetime['microsecond']  = dt.microsecond
      
      
   def todatetime(self, dic=None):
      ''' Return a datetime object '''
      if dic is None:
         dic = self.datetime
      args = [1, 1, 1, 0, 0, 0, 0, None]
      for key in _dtmap.keys():
         if key in dic:
            args[_dtmap[key]] = dic[key]
      return pydatetime(*args)
      
      
   def _fromtimestamp(self, timestamp):
      ''' Convert a timestamp to a dict '''
      self._fromdatetime(pydatetime.fromtimestamp(timestamp))
      
      
   def toisostring(self):
      ''' Convert to ISO format: YYYY-MM-DDTHH:MM:SS.SSZ '''
      iso_s = "%d-%02d-%02dT%02d:%02d:%02d.%sZ" % (
         self.datetime['year'],
         self.datetime['month'],
         self.datetime['day'],
         self.datetime['hour'],
         self.datetime['minute'],
         self.datetime['second'],
         str(self.datetime['microsecond'])[:2] )
      return iso_s
   
   
   @staticmethod
   def totimestamp(arg, utc=False):
      '''
      Return a unix timestamp from the date/time in 'arg', which can
      be a datetime object or a dictionary
      '''
      dt = None
      if type(arg) is dict:
         args = [1, 1, 1, 0, 0, 0, 0, None]
         for key in _dtmap.keys():
            if key in arg:
               args[_dtmap[key]] = arg[key]
         dt = pydatetime(*args)
      elif type(arg) is pydatetime:
         dt = arg
      else:
         raise ValueError("arg should be datetime object or a dictionary")
      
      # Use timedelta to return a timestamp
      if utc:
         return int((dt - pydatetime.utcfromtimestamp(0)).total_seconds())
      else:
         return int((dt - pydatetime.fromtimestamp(0)).total_seconds())
      
      
   @staticmethod
   def timer_start():
      _timer_time['end_time'] = _timer_time['delta_time'] = None
      _timer_time['start_time'] = pytime.time()
   
   
   @staticmethod
   def timer_end():
      _timer_time['end_time'] = pytime.time()
      _timer_time['delta_time'] = _timer_time['end_time'] - _timer_time['start_time']
      _timer_time['start_time'] = _timer_time['end_time'] = None
      return _timer_time['delta_time']
   
   

