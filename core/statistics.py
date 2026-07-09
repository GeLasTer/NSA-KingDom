"""
Statistics module for the NSA Kingdom Project.
"""
from __future__ import annotations

from core.graph import Graph
from core.BFS import BFS
from core.DFS import DFS
from models.user import User


class Statistics:
    """
    Provides statistical analysis on a Graph.

    Capabilities:
        - Total users
        - Total relationships
        - Average friends per user
        - Most connected user
        - Largest connected component
        - Distance analysis using BFS
    """

    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._bfs = BFS(graph)
        self._dfs = DFS(graph)