from types import SimpleNamespace

import numpy

from zpz.profile import timed

from pyx.datex import version01, version02, version03
from pyx.datex import cy_version09
from pyx.datex import cc_version01, cc_version02, cc_version03
from pyx.datex import c_version01


@timed
def do_them(mymod, timestamps):
    fn = mymod.weekdays
    return fn(timestamps)


@timed
def do_it(mymod, timestamps):
    fn = mymod.weekday
    return [fn(v) for v in timestamps]


def verify(x, y):
    assert all(a==b for a,b in zip(x,y))


def test_main(n = 10):
    timestamps = [i * 1000 for i in range(n)]
    timestamps_np = numpy.array(timestamps)

    print('version01')
    z1 = do_them(version01, timestamps)

    print('version02')
    z = do_them(version02, timestamps)
    verify(z, z1)

    print('version03')
    z = do_them(version03, timestamps)
    verify(z, z1)

    print('cy_version09')
    z = do_them(cy_version09, memoryview(timestamps_np))
    verify(z, z1)

    print('cc_version01')
    z = do_them(cc_version01, timestamps)
    verify(z, z1)

    print('cc_version02')
    z = do_them(cc_version02, timestamps_np)
    verify(z, z1)

    print('cc_version02 vectorized')
    a = SimpleNamespace()
    a.weekdays = cc_version02.vectorized_weekday
    z = do_them(a, timestamps_np)
    verify(z, z1)

    print('cc_version03')
    z = do_them(cc_version03, timestamps_np)
    verify(z, z1)
    # z = do_it(cc_version03, timestamps_np)
    # verify(z, z1)

    print('c_version01')
    z = do_them(c_version01, timestamps_np)
    verify(z, z1)
    # z = do_it(c_version01, timestamps_np)
    # verify(z, z1)

    z = do_them(c_version01, timestamps_np)
    # z = do_it(c_version01, timestamps_np)
    # verify(z, z1)

    z = do_them(c_version01, timestamps_np)


def main():
    test_main(1000000)


if __name__ == "__main__":
    main()


