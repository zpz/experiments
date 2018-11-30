from cffi import FFI
ffibuilder = FFI()


ffibuilder.cdef('''
    long weekday(long ts);
    void weekdays(long const * ts, long * out, long n);
    ''')

ffibuilder.set_source(
    "datex._c_version01",
    open('src/pyx/datex/_c_version01.h').read(),
    sources=['src/c/datex/c_version01.c'],
    include_dirs=['src/c/datex'],
)
