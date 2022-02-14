import math
import time
import numpy as np
import cc_nx
import cc_py
import cc_numba


def bench(mod, n_items, repeats=10):
    times_ref = []
    times_test = []

    for _ in range(repeats):
        n_components = int(math.sqrt(n_items))
        component_size = int(n_items / n_components * 0.8)
        components = [
                np.random.choice(n_items, component_size, replace=False)
                for _ in range(n_components)]

        t0 = time.perf_counter()
        _ = mod.connected_components(components, n_items)
        t1 = time.perf_counter()
        times_test.append(t1 - t0)

        t0 = time.perf_counter()
        _ = cc_nx.connected_components(components)
        t1 = time.perf_counter()
        times_ref.append(t1 - t0)

    print('')
    print('n_items:', n_items, 'n_repeats:', repeats)
    print('reference vs compare times (min max mean)')
    print('  ', f'{min(times_ref):.5f}', f'{max(times_ref):.5f}', f'{sum(times_ref)/repeats:.5f}')
    print('  ', f'{min(times_test):.5f}', f'{max(times_test):.5f}', f'{sum(times_test)/repeats:.5f}')


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('mod', choices=['py', 'nu'])
    args = parser.parse_args()

    mod = {'py': cc_py, 'nu': cc_numba}[args.mod] 

    if mod is cc_numba:
        _ = mod.connected_components([np.array([1,2,3]), np.array([0,2,3,4])], 5) 

    for n_items in (100, 1000, 10000, 100000, 500000):
        bench(mod, n_items)

