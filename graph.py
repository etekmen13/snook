from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class GraphConstraint:
    V: int  # vertices
    k: int  # color list
    cliques: tuple[tuple[int, ...], ...]  # constraints
    cliques_containing_vertex: tuple[tuple[int, ...], ...]  # inverse index
    neighbors: tuple[tuple[int, ...], ...]  # adjacency list
    neighbors_bits: tuple[tuple[int, ...], ...]  # adjacency bitset

    @staticmethod
    def build(V: int, k: int, _cliques: Sequence[Sequence[int]]) -> "GraphConstraint":
        if V <= 0:
            raise ValueError("V must be positive")
        if k <= 0:
            raise ValueError("k must be positive")

        # remove duplicates and singletons
        normalized = []
        seen = set()
        for c in _cliques:
            t = tuple(sorted(set(c)))
            if len(t) <= 1:
                continue
            if any(v < 0 or v >= V for v in t):
                raise ValueError(f"Clique has out-of-range vertex {t}")
            if t not in seen:
                seen.add(t)
                normalized.append(t)

        cliques = tuple(normalized)

        cliqvert = [[] for _ in range(V)]

        for i, c in enumerate(cliques):
            for v in c:
                cliqvert[v].append(i)

        nbr_sets = [set() for _ in range(V)]
        for c in cliques:
            L = len(c)
            for i in range(L):
                vi = c[i]
                for j in range(i + 1, L):
                    vj = c[j]
                    nbr_sets[vi].add(vj)
                    nbr_sets[vj].add(vi)

        neighbors = tuple(tuple(sorted(s)) for s in nbr_sets)
        neighbor_bits = []
        for v in range(V):
            bits = 0
            for u in neighbors[v]:
                bits |= 1 << u
            neighbor_bits.append(bits)

        return GraphConstraint(
            V=V,
            k=k,
            cliques=cliques,
            cliques_containing_vertex=tuple(tuple(x) for x in cliqvert),
            neighbors=neighbors,
            neighbors_bits=tuple(neighbor_bits),
        )


def build_rook_graph(num_rows: int, num_cols: int, num_colors: int) -> GraphConstraint:
    rows = [[i + j * num_cols for i in range(num_cols)] for j in range(num_rows)]
    cols = [[i * num_cols + j for i in range(num_rows)] for j in range(num_cols)]

    return GraphConstraint.build(
        V=num_rows * num_cols, k=num_colors, _cliques=rows + cols
    )
