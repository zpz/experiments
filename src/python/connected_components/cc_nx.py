from typing import Sequence
import networkx as nx


def connected_components(groups: Sequence[Sequence[int]]):
    graph = nx.parse_adjlist(
            (' '.join(str(i) for i in n) for n in groups),
            nodetype=int,
            )
    return nx.connected_components(graph)


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
    cc = list(connected_components(groups))
    print(cc)

    
