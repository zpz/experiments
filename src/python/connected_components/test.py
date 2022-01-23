import math
import random
import time
import numpy as np
import cc_nx
import cc_numba


COMPONENTS_1 = [
        (0, 1, 2, 3, 4, 5),
        (0, 1, 8),
        (2, 9),
        (6, 7),
        (5,),
        (8, 9),
        (10, 11, 12, 13),
        (10, 14, 15),
        ]
N_1 = 16


COMPONENTS_2 = [
        (5, 4, 3, 2, 1, 0),
        (8, 1, 0),
        (2, 9),
        (8, 9),
        (11, 13, 10, 12),
        (10, 14, 15),
        (7, 6),
        (5,),
        ]
N_2 = 16


def intro_nx():
    groups = COMPONENTS_1
    cc = cc_nx.connected_components(groups)
    print(cc)


def check_nx_sort():
    groups = COMPONENTS_2
    cc = cc_nx.connected_components(groups)
    print(cc)


def check_numba():
    groups = COMPONENTS_1
    n_items = N_1

    groups = [np.array(g) for g in groups]
    cc = cc_numba.connected_components(
            groups, n_items=n_items,
            n_components=len(groups))
    print(cc)


def _bench(n_items, repeats=1):
    for _ in range(repeats):
        n_components = int(math.sqrt(n_items))
        component_size = int(n_items / n_components * 0.8)
        components = []
        for ic in range(n_components):
            components.append(np.random.choice(
                n_items, size=component_size, replace=False))

        t0 = time.perf_counter()
        cc = cc_numba.connected_components(
                components, n_items=n_items, n_components=n_components)
        t1 = time.perf_counter()
        tnumba = t1 - t0
        print(n_items, 'numba', tnumba)

        t0 = time.perf_counter()
        cc = cc_nx.connected_components(components)
        t1 = time.perf_counter()
        tnx = t1 - t0
        print(n_items, 'networkx', tnx)

        print(n_items, tnx/tnumba)


def bench():
    for n_items in (100, 1000, 10000, 100000, 1000000, 10000000, 100000000):
        _bench(n_items, 4)



if __name__ == '__main__':
    intro_nx()
    check_nx_sort()
    check_numba()
    bench()


