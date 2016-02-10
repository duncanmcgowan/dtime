# dtime

## Simplified Python date/time convenience class

I like *datetime* but sometimes it's too complex for a trivial task; I like *time* but it's sometimes too C-like. I always seem to be passing dates and times from server to client, sometimes getting caught out by *datetime* not being JSON-serializable.

Hence **dtime**, a really simple helper class that;

<ol>
<li>Converts timestamps, strings, <i>datetime</i> objects and dictionaries to a common date/time format;</li>
<li>Converts a converted date/time entity to a <i>datetime</i> object;</li>
<li>Provides UNIX-domain timestamps;</li>
<li>Handles UTC;</li>
<li>Provides a simple timer, measuring endpoints in decimal seconds.</li>
</ol>

## Constructor

#### Initialise with current local date/time;
```
>>> import dtime
>>> dt = dtime()
>>> str(dt)
'2016-02-10 09:13:03.270588'
```

#### Initialise with a UNIX-domain timestamp;

```
>>> import dtime
>>> dt = dtime(1455095583)
>>> str(dt)
'2016-02-10 09:13:03.0'
```

#### Initialise with a user-defined dictionary

```
>>> import dtime
>>> dt = dtime (
  { 'year': 2016,
    'month': 2,
    'day': 10,
    'hour': 14,
    'minute': 21,
    'second': 9,
    'microsecond': 500 })
>>> str(dt)
'2016-02-10 14:21:09.500'
```

#### Initialise with an ISO-format string

```
>>> import dtime
>>> dt = dtime("2016-02-10T14:21:09.500Z")
>>> str(dt)
'2016-02-10 14:21:09.500'
```

#### Initialise with a *datetime* object

```
>>> import dtime
>>> from datetime import datetime
>>> dt = dtime(datetime.now())
>>> str(dt)
'2016-02-10 09:46:45.682451'
```

## Attributes

Whichever style of construction is used, **dtime** provides a common JSON-like dictionary attribute which is JSON-serializable;

```
>>> dt.datetime
{'utctimestamp': 1455114069, 'timestamp': 1455110469, 'month_str': 'February', 'month': 2, 'second': 9, 'microsecond': 500, 'year': 2016, 'timezone': None, 'day': 10, 'minute': 21, 'hour': 14, 'day_of_week': 'Wednesday'}
>>> import json
>>> s = json.dumps(dt.datetime)
>>> s
'{"utctimestamp": 1455114069, "timestamp": 1455110469, "month_str": "February", "month": 2, "second": 9, "microsecond": 500, "year": 2016, "timezone": null, "day": 10, "minute": 21, "hour": 14, "day_of_week": "Wednesday"}'
```

## Methods

#### Conversion to ISO format string

```
>>> dt.toisostring()
'2016-02-10T14:21:09.50Z'
```

#### Conversion to Python *datetime* object

```
>>> dt.todatetime()
datetime.datetime(2016, 2, 10, 9, 35, 23, 948311)
```

#### Pseudo-timer

```
>>> import dtime
>>> dtime().timer_start()
.
.
.
>>> dtime().timer_end()
>>> dtime().timer_result()
17.55080509185791
```

The pseudo-timer returns a value in decimal seconds. It is not a real timer, in that there is no background thread or process running; it is simply a calculation of delta time between a start and end time.

&copy;Duncan McGowan 2016
