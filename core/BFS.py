from __future__ import annotations

from collections import deque

from core.graph import Graph
from models.user import User


class BFS:
    """
    Provides BFS-based algorithms on top of a Graph:
        - raw traversal
        - shortest path between two users
        - distance from a source to all reachable users
    """

    def __init__(self, graph: Graph) -> None:
        self._graph = graph