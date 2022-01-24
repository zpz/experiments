from typing import Iterable 
import networkx as nx


def connected_components(components: Iterable[Iterable[int]]):
    graph = nx.parse_adjlist(
            (' '.join(str(i) for i in c) for c in components),
            nodetype=int,
            )
    return list(nx.connected_components(graph))
