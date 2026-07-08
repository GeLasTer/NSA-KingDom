from __future__ import annotations

from core.graph import Graph
from models.user import User


class DFS:
    """
    Provides DFS-based algorithms on top of a Graph:
        - simple iterative traversal
        - connected components
    Implemented iteratively (explicit stack) instead of recursively
    to avoid Python's recursion limit and function-call overhead on
    large graphs.
    """

    def __init__(self, graph: Graph) -> None:
        self._graph = graph