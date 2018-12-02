import numpy

from zpz.profile import timed

from pyx.datex import version01, version03
from pyx.datex import cy, cc, c


@timed
def do_them(fn, timestamps):
    return fn(timestamps)


def verify(x, y):
    assert all(a==b for a,b in zip(x,y))


def test_main(n = 10):
    timestamps = [i * 1000 for i in range(n)]
    timestamps_np = numpy.array(timestamps)


    print('version01')
    z1 = do_them(version01.weekdays, timestamps)

    print('version03')
    z = do_them(version03.weekdays, timestamps)
    verify(z, z1)

    print('cy_version09')
    z = do_them(cy.version09.weekdays, memoryview(timestamps_np))
    verify(z, z1)

    print('cc_version01')
    z = do_them(cc.version01.weekdays, timestamps)
    verify(z, z1)

    print('cc_version01 vectorized')
    z = do_them(cc.version01.vectorized_weekday, timestamps_np)
    verify(z, z1)

    print('cc_version02')
    z = do_them(cc.version02.weekdays, timestamps_np)
    verify(z, z1)

    print('c_version01')
    z = do_them(c.version01.weekdays, timestamps_np)
    verify(z, z1)

    z = do_them(c.version01.weekdays, timestamps_np)


def main():
    test_main(5000000)


if __name__ == "__main__":
    main()


