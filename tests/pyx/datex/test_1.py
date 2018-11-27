import numpy

from zpz.profile import timed

from pyx.datex import version01, version02, version03
from pyx.datex import cy_version09
from pyx.datex import cc_version01


@timed
def do_them(mymod, timestamps):
    fn = mymod.weekdays
    return fn(timestamps)


def verify(x, y):
    assert all(a==b for a,b in zip(x,y))


def test_main(n = 10):
    timestamps = [i * 1000 for i in range(n)]

    print('version01')
    z1 = do_them(version01, timestamps)

    print('version02')
    z = do_them(version02, timestamps)
    verify(z, z1)

    print('version03')
    z = do_them(version03, timestamps)
    verify(z, z1)

    print('cy_version09')
    z = do_them(cy_version09, memoryview(numpy.array(timestamps)))
    verify(z, z1)

    print('cc_version01')
    z = do_them(cc_version01, memoryview(numpy.array(timestamps)))
    verify(z, z1)


def main():
    test_main(1000000)


if __name__ == "__main__":
    main()


