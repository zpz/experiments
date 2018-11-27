import numpy

from zpz.profile import timed

from pyx.datex import version01, version02, version03, version04
from pyx.datex.version01 import verify


@timed
def do_them(mymod, timestamps):
    fn = mymod.weekdays
    return fn(timestamps)


if __name__ == "__main__":
    n = 1000000
    timestamps = [i * 1000 for i in range(n)]

    print('version01')
    z = do_them(version01, timestamps)
    verify(timestamps, z)

    print('version02')
    z = do_them(version02, timestamps)
    verify(timestamps, z)

    print('version03')
    z = do_them(version03, timestamps)
    verify(timestamps, z)

    print('version04')
    z = do_them(version04, memoryview(numpy.array(timestamps)))
    verify(timestamps, z)


