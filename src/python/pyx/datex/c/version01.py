from cffi import FFI
import numpy as np

from ._version01 import lib

weekday = lib.weekday

ffi = FFI()


def weekdays(ts):
    n = len(ts)
    out = np.zeros(n, dtype=np.int64)
    p_in = ffi.cast("long *", ffi.from_buffer(ts))
    p_out = ffi.cast("long *", ffi.from_buffer(out))
    lib.weekdays(p_in, p_out, n)
    return out

# _ = weekdays(np.array([1234]))
