import itertools
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
def _internal(
        item_markers: np.ndarray,
        component_markers: np.ndarray,
        idx_component: int,
        component_items: np.ndarray,
        ):
    i = idx_component
    for it in component_items:
        j = item_markers[it]
        if j < 0:
            item_markers[it] = i
        else:
            k = component_markers[j]
            if k == i:
                continue
            while True:
                component_markers[j] = i
                if k == j:
                    break
                j = k
                k = component_markers[j]


def connected_components_(
        components: Iterable[np.ndarray],
        *,
        n_items: int,
        n_components: int,
        ) -> List[np.ndarray]:
    # Each component is a sequence of items.
    # The items are represented by their indices in the entire set of items
    # across all components, hence all the elements in `components`
    # are integers from 0 up to but not including `n_items`, which
    # is the total numbe of items across all components.

    item_markers = np.full(n_items, -1)
    component_markers = np.arange(n_components)

    for i, component_items in enumerate(components):
        _internal(item_markers, component_markers, i, component_items)

    groups = defaultdict(list)
    # Each element is a list of component indices;
    # these components are connected.
    for i, mark in enumerate(component_markers):
        if mark != i:
            k = component_markers[mark]
            while k != mark:
                mark = k
                k = component_markers[mark]
        groups[mark].append(i)

    return list(groups.values())


def connected_components(components, **kwargs):
    cc = connected_components_(components, **kwargs)

    return cc

    return [
            sorted(set(itertools.chain.from_iterable(
                (components[idx] for idx in c))))
            for c in cc
            ]

