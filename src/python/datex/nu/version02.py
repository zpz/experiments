from numba import jit
from .version01 import weekday


@jit(nopython=True)
def weekdays(ts):
    return [weekday(v) for v in ts]