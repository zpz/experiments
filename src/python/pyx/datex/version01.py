from datetime import datetime


def weekday(ts):
    dt = datetime.utcfromtimestamp(ts)
    wd = dt.isoweekday()
    return wd


def weekdays(ts):
    return [weekday(t) for t in ts] 


def verify(timestamps, results):
    for x, y in zip(timestamps, results):
        yy = weekday(x)
        assert y == yy
