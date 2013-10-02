"""This is the helper for :class:`datetime.datetime`. 
    Dealing with the operations related to datetime.
"""

from datetime import datetime, timedelta

oneday = timedelta(days=1)
"""A one day timedelta object."""
onehour = timedelta(seconds=3600)
"""A one hour timedelta object."""
tenminutes = timedelta(seconds=600)
"""A ten minutes timedelta object."""
oneminute = timedelta(seconds=60)
"""A one minute timedelta object."""

def floorbyhour(input_datetime):
    """Return the floored datetime versus hour from input_datetime."""
    d = timedelta(seconds=(input_datetime.minute*60+input_datetime.second),microseconds=input_datetime.microsecond)
    return input_datetime-d

def floorbyday(input_datetime, hour_shift=0):
    """Return the floored datetime versus day from input_datetime."""
    time_shift = timedelta(seconds=hour_shift*360)
    input_datetime -= time_shift
    d = timedelta(seconds=(input_datetime.hour*3600+input_datetime.minute*60+input_datetime.second),microseconds=input_datetime.microsecond)
    input_datetime += time_shift
    return input_datetime-d

def timetoclock(cal_time):
    """Return an int indicates the clock of the cal_time. The value range from 0 to 23."""
    return int(cal_time/3600)%24
