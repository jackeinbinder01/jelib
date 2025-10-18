import heapq
from collections import deque

'''
UNINFORMED SEARCH ALGORITHMS
'''


def dfs(graph, start, goal, heuristic, report):
    print("Conducting DFS...\n")

    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            report(
                expanded_node=current,
                g_cost=None,
                h_cost=None,
                path=path,
                frontier=sorted([(n, None) for n, _ in stack if n not in visited])
            )
            return path

        frontier_nodes = set(n for n, _ in stack)
        for neighbor in reversed(list(graph.neighbors(current))):
            if neighbor not in visited and neighbor not in frontier_nodes:
                stack.append((neighbor, path + [neighbor]))

        report(
            expanded_node=current,
            g_cost=None,
            h_cost=None,
            path=path,
            frontier=sorted([(n, None) for n, _ in stack if n not in visited])
        )

    return None


def depth_limited_dfs(graph, current, goal, limit, path, visited, report):
    if current == goal:
        report(
            expanded_node=current,
            g_cost=None,
            h_cost=None,
            path=path,
            frontier=[]
        )
        return path

    report(
        expanded_node=current,
        g_cost=None,
        h_cost=None,
        path=path,
        frontier=[]
    )

    if limit == 0:
        return None

    visited.add(current)
    for neighbor in graph.neighbors(current):
        if neighbor not in visited:
            result = depth_limited_dfs(
                graph,
                neighbor,
                goal,
                limit - 1,
                path + [neighbor],
                visited,
                report
            )
            if result:
                return result
    visited.remove(current)
    return None


def iterative_deepening_dfs(graph, start, goal, heuristic, report):
    print("Conducting Iterative Deepening DFS...\n")

    depth = 0
    while True:
        print(f"Trying depth limit: {depth}")
        visited = set()
        result = depth_limited_dfs(
                graph,
                start,
                goal,
                depth,
                [start],
                visited,
                report
            )
        if result:
            return result
        depth += 1


def bfs(graph, start, goal, heuristic, report):
    print("Conducting BFS...\n")

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            report(
                expanded_node=current,
                g_cost=None,
                h_cost=None,
                path=path,
                frontier=sorted([(n, None) for n, _ in queue if n not in visited])
            )
            return path

        frontier_nodes = set(n for n, _ in queue)
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and neighbor not in frontier_nodes:
                queue.append((neighbor, path + [neighbor]))

        report(
            expanded_node=current,
            g_cost=None,
            h_cost=None,
            path=path,
            frontier=sorted([(n, None) for n, _ in queue if n not in visited])
        )

    return None


def ucs(graph, start, goal, heuristic, report):
    print("Conducting UCS...\n")

    frontier = [(0, start, [start])]
    visited = set()

    while frontier:
        g, current, path = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            report(
                expanded_node=current,
                g_cost=g,
                h_cost=None,
                path=path,
                frontier=sorted([(n, g_) for g_, n, _ in frontier if n not in visited])
            )
            return path

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                edge_weight = graph[current][neighbor].get("weight", 1)
                new_g = g + edge_weight
                heapq.heappush(frontier, (new_g, neighbor, path + [neighbor]))

        report(
            expanded_node=current,
            g_cost=g,
            h_cost=None,
            path=path,
            frontier=sorted(
                [(n, g_) for g_, n, _ in frontier if n not in visited],
                key=lambda x: x[1]
            )
        )

    return None


def bidirectional_search(graph, start, goal, heuristic, report):
    print("Conducting Bidirectional Search...\n")

    frontier_start = deque([(start, [start])])
    frontier_goal = deque([(goal, [goal])])

    visited_start = {start: [start]}
    visited_goal = {goal: [goal]}

    def expand_frontier(frontier, visited_self, visited_other, direction):
        current, path = frontier.popleft()

        for neighbor in graph.neighbors(current):
            if neighbor not in visited_self:
                visited_self[neighbor] = path + [neighbor]
                frontier.append((neighbor, path + [neighbor]))

                if neighbor in visited_other:
                    report(
                        expanded_node=neighbor,
                        g_cost=None,
                        h_cost=None,
                        path=visited_self[neighbor],
                        frontier=sorted([(n, None) for n, _ in frontier if n not in visited_self])
                    )

                    path_from_start = visited_start[neighbor]
                    path_from_goal = visited_goal[neighbor]
                    if direction == "forward":
                        return path_from_start + path_from_goal[-2::-1]
                    else:
                        return path_from_goal + path_from_start[-2::-1]

        report(
            expanded_node=current,
            g_cost=None,
            h_cost=None,
            path=path,
            frontier=sorted([(n, None) for n, _ in frontier if n not in visited_self])
        )

        return None

    while frontier_start and frontier_goal:
        result = expand_frontier(frontier_start, visited_start, visited_goal, "forward")
        if result:
            return result

        result = expand_frontier(frontier_goal, visited_goal, visited_start, "backward")
        if result:
            return result

    return None


'''
INFORMED SEARCH ALGORITHMS
'''


def a_star(graph, start, goal, heuristic, report):
    print("Conducting A* Search...\n")

    start_g = 0
    start_h = heuristic(start)
    start_f = start_g + start_h
    frontier = [(start_f, start_g, start, [start])]
    visited = {}

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current in visited and g >= visited[current]:
            continue
        visited[current] = g



        if current == goal:
            report(
                expanded_node=current,
                g_cost=g,
                h_cost=heuristic(current),
                path=path,
                frontier=sorted(
                    [(n, g_ + heuristic(n)) for f_, g_, n, _ in frontier if n not in visited],
                    key=lambda x: x[1]
                )
            )
            return path

        for neighbor in graph.neighbors(current):
            edge_weight = graph[current][neighbor].get("weight", 1)
            new_g = g + edge_weight
            new_h = heuristic(neighbor)
            new_f = new_g + new_h
            heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))

        report(
            expanded_node=current,
            g_cost=g,
            h_cost=heuristic(current),
            path=path,
            frontier=sorted(
                [(n, g_ + heuristic(n)) for f_, g_, n, _ in frontier if n not in visited],
                key=lambda x: x[1]
            )
        )

    return None


def greedy_search(graph, start, goal, heuristic, report):
    print("Conducting Greedy Search...\n")

    frontier = [(heuristic(start), start, [start])]
    visited = set()

    while frontier:
        h, current, path = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            report(
                expanded_node=current,
                g_cost=None,
                h_cost=heuristic(current),
                path=path,
                frontier=sorted(
                    [(n, h_) for h_, n, _ in frontier if n not in visited],
                    key=lambda x: x[1]
                )
            )
            return path

        frontier_nodes = set(n for _, n, _ in frontier)
        for neighbor in graph.neighbors(current):
            if neighbor not in visited and neighbor not in frontier_nodes:
                new_h = heuristic(neighbor)
                heapq.heappush(frontier, (new_h, neighbor, path + [neighbor]))

        report(
            expanded_node=current,
            g_cost=None,
            h_cost=heuristic(current),
            path=path,
            frontier=sorted(
                [(n, h_) for h_, n, _ in frontier if n not in visited],
                key=lambda x: x[1]
            )
        )

    return None
