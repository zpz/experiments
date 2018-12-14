import numpy as np
cimport numpy as np
cimport cython


@cython.cdivision(True)
cdef long weekday(long ts):
    cdef long ts0, weekday0, DAY_SECONDS, WEEK_SECONDS
    cdef long ts_delta, td, nday, weekday

    ts0 = 1489363200   # 2017-03-13 0:0:0 UTC, Monday
    weekday0 = 1   # ISO weekday: Monday is 1, Sunday is 7

    DAY_SECONDS = 86400
    WEEK_SECONDS = 604800

    ts_delta = ts - ts0
    if ts_delta < 0:
        ts_delta += ((-ts_delta) // WEEK_SECONDS + 1) * WEEK_SECONDS

    td = ts_delta % WEEK_SECONDS
    nday = td // DAY_SECONDS
    weekday = weekday0 + nday
    if weekday > 7:
        weekday = weekday - 7
    return weekday


def weekdays(long[:] ts):
    cdef long n = len(ts)
    cdef np.ndarray[np.int64_t, ndim=1] out = np.empty(n, np.int64)
    cdef long[:] oout = memoryview(out)
    cdef long i, t, z
    for i in range(n):
        t = ts[i]
        z = weekday(t)
        oout[i] = z
    return out
