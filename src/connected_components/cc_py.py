import itertools
from collections import defaultdict
from typing import List


def _internal(components: List[List[int]], n_items):
    item_markers = [-1 for _ in range(n_items)]
    component_markers = list(range(len(components)))

    for i, component_items in enumerate(components):
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

    return component_markers


def connected_components_(components: List[List[int]], n_items):
    component_markers = _internal(components, n_items)

    groups = defaultdict(list)

    for i, mark in enumerate(component_markers):
        if mark != i:
            k = component_markers[mark]
            while k != mark:
                mark = k
                k = component_markers[mark]
        groups[mark].append(i)

    return list(groups.values())


def connected_components(components: List[List[int]], n_items):
    cc = connected_components_(components, n_items)

    return [
            set(itertools.chain.from_iterable(
                (components[idx] for idx in c)))
            for c in cc
            ]

