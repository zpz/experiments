from functools import partial
import numpy

from zpz.profile import Timer

from pyx.datex import version01, version03
from pyx.datex import cy, cc, c, nu


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
    print('{: <42}:  {: >8.4f} seconds'.format(name, t))


def do_all(fn, n):
    timestamps_np = numpy.random.randint(10000000, 9999999999, size=n, dtype=numpy.int64)

    functions = [
        (version01.weekdays, timestamps_np),
        (version03.weekdays, timestamps_np),
        (cy.version09.weekdays, memoryview(timestamps_np)),
        (cc.version01.weekdays, memoryview(timestamps_np)),
        (cc.version01.vectorized_weekday, timestamps_np),
        (cc.version02.weekdays, timestamps_np),
        (c.version01.weekdays, timestamps_np),
        (nu.version01.weekdays, timestamps_np),
        (nu.version02.weekdays, timestamps_np),
        (nu.version03.weekdays, timestamps_np),
        (nu.version04.weekdays, timestamps_np),
    ]

    _ = c.version01.weekdays(timestamps_np[:10])
    _ = nu.version01.weekdays(timestamps_np[:10])
    _ = nu.version02.weekdays(timestamps_np[:10])
    _ = nu.version03.weekdays(timestamps_np[:10])
    _ = nu.version04.weekdays(timestamps_np[:10])

    for f, ts in functions:
        fn(f, ts)


def test_all():
    do_all(check_it, 10)


def benchmark(n, repeat):
    do_all(partial(time_it, repeat=repeat), n)


if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--n', type=int, default=10000000)
    p.add_argument('--repeat', type=int, default=1)
    args = p.parse_args()

    benchmark(args.n, args.repeat)


