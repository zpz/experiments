import math
import time
import numpy as np
import cc_nx
import cc_py
import cc_numba


def bench(mod, n_items, repeats=10):
    for _ in range(repeats):
        n_components = int(math.sqrt(n_items))
        component_size = int(n_items / n_components * 0.8)
        components = [
                np.random.choice(n_items, component_size, replace=False)
                for _ in range(n_components)]

        t0 = time.perf_counter()
        _ = mod.connected_components(components, n_items)
        t1 = time.perf_counter()
        tpy = t1 - t0

        t0 = time.perf_counter()
        _ = cc_nx.connected_components(components)
        t1 = time.perf_counter()
        tnx = t1 - t0

        print(n_items, f'{tnx:.6f}', f'{tpy:.6f}', f'{tnx/tpy:.2f}')


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('mod', choices=['py', 'nu'])
    args = parser.parse_args()

    mod = {'py': cc_py, 'nu': cc_numba}[args.mod] 
    for n_items in (1000, 10000, 100000, 1000000):
        bench(mod, n_items)

