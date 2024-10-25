import networkx as nx
from networkx.algorithms.community import girvan_newman
from typing import TypeAlias
import matplotlib.pyplot as plt
from pprint import pprint

t_wiring: TypeAlias = dict[str, list[str]]


def main() -> None:
    nodes = set()
    edges = list()
    wiring: t_wiring = dict()

    with open("2023//Day25//input.txt") as f:
        g_wiring = nx.Graph()
        for line in f.readlines():
            from_component = line.split(":")[0]
            wiring[line.split(":")[0]] = line.split(": ")[1].split()

        for l_comp, r_comps in wiring.items():
            nodes.add(l_comp)
            for comp in r_comps:
                nodes.add(comp)
                edges.append((l_comp, comp))

        g_wiring.add_nodes_from(nodes)
        g_wiring.add_edges_from(edges)

        communities = list(next(girvan_newman(g_wiring)))

        ans = 1

        for community in communities:
            ans *= len(community)

        print(ans)

        # nx.draw(g_wiring, with_labels=True, node_color="skyblue")
        # plt.show()


if __name__ == "__main__":
    main()
