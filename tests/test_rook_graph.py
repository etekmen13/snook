from collections import Counter

from snook.graph import build_rook_graph, GraphConstraint


def clique_check(g: GraphConstraint, rows: int, cols: int) -> bool:
    """
    Ensure each vertex appears in exactly two cliques
    (one row + one column for rook graphs).
    """
    cnt = Counter()
    for c in g.cliques:
        for v in c:
            cnt[v] += 1
    expected = (1 if cols > 1 else 0) + (1 if rows > 1 else 0)
    return all(cnt[v] == expected for v in range(g.V))


def degree_check(g: GraphConstraint, rows: int, cols: int) -> bool:
    """
    Ensure each vertex has degree rows + cols - 2.
    """
    target = rows + cols - 2
    return all(bits.bit_count() == target for bits in g.neighbors_bits)


def adjacency_check(g: GraphConstraint) -> None:
    """
    Ensure symmetric and nonreflexive adjacency.
    """
    for i in range(g.V):
        # nonreflexive
        assert ((g.neighbors_bits[i] >> i) & 1) == 0

        # symmetry
        for j in range(g.V):
            ij = (g.neighbors_bits[i] >> j) & 1
            ji = (g.neighbors_bits[j] >> i) & 1
            assert ij == ji


def inverse_index_check(g: GraphConstraint) -> None:
    """
    Ensure cliques_containing_vertex matches cliques.
    """
    for v in range(g.V):
        expected = tuple(i for i, c in enumerate(g.cliques) if v in c)
        assert g.cliques_containing_vertex[v] == expected


def test_rook_graph():
    for rows in range(1, 6):
        for cols in range(1, 6):
            k = max(rows, cols)
            g = build_rook_graph(rows, cols, k)

            assert g.V == rows * cols
            assert clique_check(g, rows, cols)
            assert degree_check(g, rows, cols)
            adjacency_check(g)
            inverse_index_check(g)


def test_rook_graph_2x3_neighbors():
    g = build_rook_graph(2, 3, 3)

    # vertex layout:
    # 0 1 2
    # 3 4 5

    expected = {
        0: {1, 2, 3},
        1: {0, 2, 4},
        2: {0, 1, 5},
        3: {0, 4, 5},
        4: {1, 3, 5},
        5: {2, 3, 4},
    }

    for v in range(g.V):
        assert set(g.neighbors[v]) == expected[v]
