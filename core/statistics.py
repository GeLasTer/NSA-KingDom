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
    # =====================================================
    # Basic Statistics
    # =====================================================

    def total_users(self) -> int:
        """
        Return total number of users.
        """
        return self._graph.node_count()

    def total_relationships(self) -> int:
        """
        Return total number of friendships.
        """
        return self._graph.edge_count()

    def average_friends(self) -> float:
        """
        Return average number of friends per user.

        Formula:
            (2 × edges) / users
        """

        users = self.total_users()

        if users == 0:
            return 0.0

        return (2 * self.total_relationships()) / users      
    # =====================================================
    # Degree Analysis
    # =====================================================

    def most_connected_user(self) -> User | None:
        """
        Return the user with the highest number of friendships.

        Returns:
            User object if graph is not empty.
            None if graph has no users.
        """

        if self.total_users() == 0:
            return None

        best_id = max(
            self._graph.user_ids(),
            key=self._graph.degree
        )

        return self._graph.get_user(best_id)

    # =====================================================
    # Connected Components
    # =====================================================

    def _largest_component(self) -> list[int]:
        """
        Internal helper.

        Finds and returns the largest connected component.

        Returns:
            List of user IDs belonging to the largest component.
        """

        components = self._dfs.connected_components()

        if not components:
            return []

        return max(components, key=len)

    def largest_group_size(self) -> int:
        """
        Return size of the largest friendship group.
        """

        return len(self._largest_component())

    def largest_group_members(self) -> list[User]:
        """
        Return the users belonging to the largest friendship group.
        """

        return [
            self._graph.get_user(user_id)
            for user_id in self._largest_component()
        ]