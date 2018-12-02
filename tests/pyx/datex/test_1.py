from functools import partial
import numpy

from zpz.profile import Timer

from pyx.datex import version01, version03
from pyx.datex import cy, cc, c



def check_it(fn, timestamps):
    z = fn(timestamps)
    z0 = version01.weekdays(timestamps)
    assert all(a == b for a,b in zip(z, z0))


def time_it(fn, timestamps, repeat=1):
    tt = Timer().start()
    for _ in range(repeat):
        z = fn(timestamps)
    t = tt.stop().seconds
    name = fn.__module__ + '.' + fn.__name__
    print('{: <42}:  {: >6.4f} seconds'.format(name, t))


def do_all(fn, n):
    timestamps = [i * 1000 for i in range(n)]
    timestamps_np = numpy.array(timestamps)

    functions = [
        (version01.weekdays, timestamps),
        (version03.weekdays, timestamps),
        (cy.version09.weekdays, memoryview(timestamps_np)),
        (cc.version01.weekdays, memoryview(timestamps_np)),
        (cc.version01.vectorized_weekday, timestamps_np),
        (cc.version02.weekdays, timestamps_np),
        (c.version01.weekdays, timestamps_np),
        (c.version01.weekdays, timestamps_np),
    ]

    for f, ts in functions:
        fn(f, ts)


def test_all():
    do_all(check_it, 10)


def benchmark(n, repeat):
    do_all(partial(time_it, repeat=repeat), n)
    

if __name__ == "__main__":
    benchmark(1000000, 100)


