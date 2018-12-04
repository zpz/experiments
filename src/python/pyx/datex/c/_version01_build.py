from cffi import FFI
ffibuilder = FFI()


ffibuilder.cdef(open('src/c/datex/c_version01.h').read())

ffibuilder.set_source(
    "datex.c._version01",
    '',
    sources=['src/c/datex/c_version01.c'],
    include_dirs=['src/c/datex'],
)

# The paths in the code above are relative to the location
# of `setup.py`, which calls this script.