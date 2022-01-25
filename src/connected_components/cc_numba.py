import itertools
from collections import defaultdict
from typing import List, Iterable, Sequence

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
        i_component: int,
        component_items: np.ndarray,
        ):
    for item in component_items:
        j_component = item_markers[item]

        if j_component < 0:
            item_markers[item] = i_component
        else:
            if component_markers[j_component] == i_component:
                continue

            while True:
                k_group = component_markers[j_component]
                component_markers[j_component] = i_component
                if k_group == j_component:
                    break
                j_component = k_group


def connected_components(components: Sequence[Sequence[int]], n_items: int):
    components = [
            c if isinstance(c, np.ndarray) else np.array(c)
            for c in components
            ]
    n_components = len(components)

    item_markers = np.full(n_items, -1)
    component_markers = np.arange(n_components)

    for i, component_items in enumerate(components):
        _internal(item_markers, component_markers, i, component_items)

    for i in reversed(range(n_components - 1)):
        if (k := component_markers[i]) != i:
            component_markers[i] = component_markers[k]

    item_markers = item_markers[item_markers >= 0]
    item_markers = component_markers[item_markers]

    return [
            np.where(item_markers == v)[0]
            for v in np.unique(component_markers)
            ]

