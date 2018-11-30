from cffi import FFI

from ._c_version01 import lib

weekday = lib.weekday


def weekdays(ts):
    ffi = FFI()
    ts = ffi.new('long[]', ts)
    out = ffi.new('long[]', len(ts))
    lib.weekdays(ts, out, len(ts))
    return out