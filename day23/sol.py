from collections import defaultdict

def part1(graph):
    # find 3-length cliques
    cliques = set()
    for node in graph:
        for neighbor1 in graph[node]:
            for neighbor2 in graph[neighbor1]:
                if neighbor2 in graph[node]:
                    if node.startswith('t'):
                        clique = tuple(sorted([node, neighbor1, neighbor2]))
                        cliques.add(clique)
    
    return len(cliques)

# classic Bron-Kerbosch algorithm
def BronKerbosch(R, P, X, graph, cliques):
    if len(P) == 0 and len(X) == 0:
        cliques.add(tuple(sorted(R)))
    for v in P.copy():
        R_new = R.copy()
        R_new.add(v)
        P_new = P.intersection(graph[v])
        X_new = X.intersection(graph[v])
        BronKerbosch(R_new, P_new, X_new, graph, cliques)
        P.remove(v)
        X.add(v)

def part2(graph):
    cliques = set()
    BronKerbosch(set(), set(graph.keys()), set(), graph, cliques)
    max_clique_size = max([len(clique) for clique in cliques])
    max_clique = [clique for clique in cliques if len(clique) == max_clique_size]
    return ",".join(max_clique[0])

def solve(input):
    with open(input) as file:
        edges = [line.strip().split('-') for line in file.readlines()]
        graph = defaultdict(set)
        for edge in edges:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])


    return (part1(graph), part2(graph))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])