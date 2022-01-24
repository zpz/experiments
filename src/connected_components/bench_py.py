import math
import random
import time
import numpy as np
import cc_nx
import cc_py


def bench(n_items, repeats=1):
    population = list(range(n_items))
    for _ in range(repeats):
        n_components = int(math.sqrt(n_items))
        component_size = int(n_items / n_components * 0.8)
        components = [random.sample(population, component_size) for _ in range(n_components)]

        t0 = time.perf_counter()
        _ = cc_py.connected_components(components, n_items)
        t1 = time.perf_counter()
        tpy = t1 - t0

        t0 = time.perf_counter()
        _ = cc_nx.connected_components(components)
        t1 = time.perf_counter()
        tnx = t1 - t0

        print(n_items, f'{tnx:.6f}', f'{tpy:.6f}', f'{tnx/tpy:.2f}')


if __name__ == '__main__':
    for n_items in (100, 1000, 10000, 100000, 1000000, 10000000, 100000000):
        bench(n_items, 4)

