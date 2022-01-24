from typing import Sequence
import networkx as nx


def connected_components(groups: Sequence[Sequence[int]]):
    graph = nx.parse_adjlist(
            (' '.join(str(i) for i in n) for n in groups),
            nodetype=int,
            )
    return list(nx.connected_components(graph))
