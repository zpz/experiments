from collections import defaultdict
from typing import List, Iterable

import numba
import numpy as np


# Numba cache of the compiled function is in __pycache__
# in the directory of the source code.
# First run of this function includes compilation time.
# Compiling this function in particular prints a warning;
# don't worry about it.
@numba.jit(nopython=True, cache=True)
def _connected_components_internal(
        item_markers: np.ndarray,
        neighborhood_markers: np.ndarray,
        idx_neighborhood: int,
        neighbors: np.ndarray,
        ):
    i = idx_neighborhood
    for it in neighbors:
        j = item_markers[it]
        if j < 0:
            item_markers[it] = i
        else:
            k = neighborhood_markers[j]
            if k == i:
                continue
            while True:
                neighborhood_markers[j] = i
                if k == j:
                    break
                j = k
                k = neighborhood_markers[j]


def connected_components(
        neighborhoods: Iterable[np.ndarray],
        *,
        n_items: int,
        n_neighborhoods: int,
        ) -> List[np.ndarray]:
    # Each neighborhood is a sequence of items.
    # The items are represented by their indices in the entire set of items
    # across all neighborhoods, hence all the elements in `neighborhoods`
    # are integers from 0 up to but not including `n_items`, which
    # is the total numbe of items across all neighborhoods.

    item_markers = np.full(n_items, -1)
    neighborhood_markers = np.arange(n_neighborhoods)

    for i, neighbors in enumerate(neighborhoods):
        _connected_components_internal(item_markers, neighborhood_markers, i, neighbors)

    groups = defaultdict(list)
    # Each element is a list of neighborhood indices;
    # these neighborhoods are connected.
    for i, mark in enumerate(neighborhood_markers):
        if mark != i:
            k = neighborhood_markers[mark]
            while k != mark:
                mark = k
                k = neighborhood_markers[mark]
        groups[mark].append(i)

    return list(groups.values())



if __name__ == '__main__':
    groups = [
            (0, 1, 2, 3, 4, 5),
            (0, 1, 8),
            (2, 9),
            (6, 7),
            (5,),
            (8, 9),
            (10, 11, 12, 13),
            (10, 14, 15),
            ]
    groups = [np.array(g) for g in groups]
    cc = list(connected_components(groups, n_items=16, n_neighborhoods=len(groups)))
    print(cc)

