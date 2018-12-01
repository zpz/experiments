from cffi import FFI
import numpy as np

from ._c_version01 import lib

weekday = lib.weekday

ffi = FFI()


def weekdays(ts):
    out = np.zeros(len(ts), dtype=np.int64)
    lib.weekdays(
        ffi.cast("long *", ffi.from_buffer(ts)),
        ffi.cast("long *", ffi.from_buffer(out)), 
        len(ts))
    return out


_ = weekdays(np.array([1234]))