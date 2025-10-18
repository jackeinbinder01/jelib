import networkx as nx


class GraphTracer:
    def __init__(self, graph: nx.Graph, heuristic=None):
        self.graph = graph
        self.heuristic = heuristic or (lambda n: 0)
        self.expansion_order = []

    def trace(self, algorithm, start, goal=None):
        print("Searching...\n")
        result = algorithm(self.graph, start, goal, self.heuristic, self._report)
        print("\nGoal reached!" if result else "\nNo result found")

    def _report(self, expanded_node, g_cost, h_cost, path, frontier):
        self.expansion_order.append(expanded_node)
        print(f"Node Expanded: {expanded_node}")

        if g_cost is not None:
            print(f"g(n): {g_cost}")
        if h_cost is not None:
            print(f"h(n): {h_cost}")
        if g_cost is not None and h_cost is not None:
            print(f"f(n): {g_cost + h_cost}")

        print("Expansion Order:", " -> ".join(self.expansion_order))
        print("Path:", " -> ".join(path))
        print("Frontier:", ", ".join(f"{n} (f(n)={c})" for n, c in frontier))
        print()



