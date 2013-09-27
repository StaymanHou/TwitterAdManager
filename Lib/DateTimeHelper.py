from datetime import datetime, timedelta

oneday = timedelta(days=1)
onehour = timedelta(seconds=3600)
tenminutes = timedelta(seconds=600)
oneminute = timedelta(seconds=60)

def floorbyhour(input_datetime):
    d = timedelta(seconds=(input_datetime.minute*60+input_datetime.second),microseconds=input_datetime.microsecond)
    return input_datetime-d

def floorbyday(input_datetime, hour_shift=0):
    time_shift = timedelta(seconds=hour_shift*360)
    input_datetime -= time_shift
    d = timedelta(seconds=(input_datetime.hour*3600+input_datetime.minute*60+input_datetime.second),microseconds=input_datetime.microsecond)
    input_datetime += time_shift
    return input_datetime-d

def timetoclock(cal_time):
    return int(cal_time/3600)%24
