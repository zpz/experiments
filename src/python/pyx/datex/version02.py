from datetime import datetime
import pytz


class TimestampShifter:
    DAY_SECONDS = 86400
    WEEK_SECONDS = 604800

    def __init__(self):
        basedate = datetime.now(pytz.timezone('utc'))
        self._weekday = basedate.isoweekday()  # Monday is 1, Sunday is 7
        dt = basedate.replace(hour=0, minute=0, second=0, microsecond=0)
        self._timestamp = int(dt.timestamp())

    def shift_to(self, ts):
        ts_delta = ts - self._timestamp
        if ts_delta < 0:
            ts_delta += ((-ts_delta) // self.WEEK_SECONDS + 1) * self.WEEK_SECONDS

        td = ts_delta % self.WEEK_SECONDS
        nday = td // self.DAY_SECONDS
        weekday = self._weekday + int(nday)
        if weekday > 7:
            weekday = weekday - 7
        return weekday


def weekday(ts):
    shifter = TimestampShifter()
    z = shifter.shift_to(ts)
    return z


def weekdays(ts):
    shifter = TimestampShifter()
    return [shifter.shift_to(t) for t in ts]
