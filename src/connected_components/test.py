import numpy as np
import cc_nx
import cc_py
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
        (7, 6),
        (5, 4, 3, 2, 1, 0),
        (8, 1, 0),
        (2, 9),
        (8, 9),
        (11, 13, 10, 12),
        (10, 14, 15),
        (5,),
        ]
N_2 = 16


def intro_nx():
    cc = cc_nx.connected_components(COMPONENTS_1)
    print(cc)


def check_nx():
    cc = cc_nx.connected_components(COMPONENTS_2)
    print(cc)


def check_py(mod):
    cc = mod.connected_components(COMPONENTS_2, N_2)
    print(mod.__name__)
    print(cc)


if __name__ == '__main__':
    intro_nx()
    check_nx()
    check_py(cc_py)
    check_py(cc_numba)


