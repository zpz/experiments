import numpy as np
from numba import jit

from .version01 import weekday


@jit(nopython=True)
def weekdays(ts):
    n = len(ts)
    out = np.zeros(n, dtype=np.int64)
    for i, v in enumerate(ts):
        out[i] = weekday(v)
    return out