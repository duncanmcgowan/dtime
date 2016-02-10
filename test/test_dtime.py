import unittest
import dtime
import json
from datetime import datetime as pydatetime
import time as pytime

'''
From the directory above the directory containing this module...

>>> python -m unittest test.test_dtime

DM 2016
'''

class test_dtime_constructor(unittest.TestCase):
   
   def setUp(self):
      
      self.iso_string = "2016-02-10T12:34:23.500Z"
      self.utctimestamp = 1455107663
      self.datetimeobject = pydatetime(2016, 2, 10, 12, 34, 23, 500, None)
      self.userdefined = {'year'         : 2016,
                          'month'        : 2,
                          'day'          : 10,
                          'hour'         : 12,
                          'minute'       : 34,
                          'second'       : 23,
                          'microsecond'  : 5000 }
      
   def tearDown(self):
      pass
   
   def testConstructor(self):
      
      dt = dtime(self.iso_string)
      assert type(dt) is not None
      assert dt.datetime['utctimestamp'] == 1455107663
      
      dt = dtime(self.utctimestamp)
      assert type(dt) is not None
      
      dt = dtime(self.datetimeobject)
      assert type(dt) is not None
      assert dt.datetime['utctimestamp'] == 1455107663
      
      dt = dtime(self.userdefined)
      assert type(dt) is not None
      assert dt.datetime['utctimestamp'] == 1455107663
      
      dt = dtime()
      assert type(dt) is not None
      assert dt.__class__.OBJECT_NAME == "dtime"
      

class test_dtime_json_serializable(unittest.TestCase):
   
   def setUp(self):
      self.iso_string = "2016-02-10T12:34:23.500Z"
        
   def tearDown(self):
      pass
   
   def testSerializableAndBackAgain(self):
      
      dt = dtime(self.iso_string)
      assert type(dt.datetime) == dict
      assert dt.datetime['utctimestamp'] == 1455107663
      s = json.dumps(dt.datetime)
      assert type(s) == str
      d = json.loads(s)
      dt = dtime(d)
      assert type(dt.datetime) == dict
      assert dt.datetime['utctimestamp'] == 1455107663
      
      
class test_dtime_datetime_object(unittest.TestCase):
   
   def setUp(self):
      self.iso_string = "2016-02-10T12:34:23.500Z"
      
   def tearDown(self):
      pass
   
   def testDatetimeObject(self):
      
      dt = dtime(self.iso_string)
      dto = dt.todatetime()
      assert type(dto) is pydatetime
      
      
class test_dtime_isostring(unittest.TestCase):
   
   def setUp(self):
      self.utctimestamp = 1455107663
      
   def tearDown(self):
      pass
   
   def testISOString(self):
      
      dt = dtime(self.utctimestamp)
      s = dt.toisostring()
      assert type(s) is str
      assert dt.datetime['year'] == 2016
      assert dt.datetime['month'] == 2
      assert dt.datetime['day'] == 10
      assert s.find("Z") > -1
      
      
class test_dtime_timer(unittest.TestCase):
   
   def testTimer(self):
      
      dtime().timer_start()
      pytime.sleep(2)
      dtime().timer_end()
      assert dtime().timer_result() > 1.9
      assert dtime().timer_result() < 2.1
      

if __name__ == '__main__':
   unittest.main()
   