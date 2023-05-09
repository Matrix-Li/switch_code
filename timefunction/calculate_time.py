import datetime
from skyfield.api import load


def calculate_start_end_time(_seconds):
    # record current time
    current_time = str(datetime.datetime.now())
    year = (float)(current_time[0:4])
    month = (float)(current_time[5:7])
    day = (float)(current_time[8:10])
    hour = (float)(current_time[11:13])
    minute = (float)(current_time[14:16])
    second = (float)(current_time[17:-1])
    end_time = str(datetime.datetime.now() +
                   datetime.timedelta(seconds=_seconds))
    #t0 is begin, t1 is end
    ts = load.timescale()
    t0 = ts.utc(year, month, day, hour, minute, second)
    year = (float)(end_time[0:4])
    month = (float)(end_time[5:7])
    day = (float)(end_time[8:10])
    hour = (float)(end_time[11:13])
    minute = (float)(end_time[14:16])
    second = (float)(end_time[17:-1])
    t1 = ts.utc(year, month, day, hour, minute, second)
    return t0, t1


# t1 - t0
def time_difference_seconds(t0, t1):
    t_0 = datetime.datetime.strptime(t0, '%Y %m %d %H:%M:%S')
    t_1 = datetime.datetime.strptime(t1, '%Y %m %d %H:%M:%S')
    difference = (t_1-t_0).seconds
    return difference
