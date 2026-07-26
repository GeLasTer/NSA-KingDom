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
        # Reuse existing BFS and DFS implementations.
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
            # Avoid division by zero when graph is empty.
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
        
# Select the user with the highest degree.
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

    # Get all connected components using DFS.
        components = self._dfs.connected_components()

        if not components:
            return []
    # Return the largest component.
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

    # =====================================================
    # BFS Analysis
    # =====================================================

    def distance_analysis(self, source_id: int | str) -> dict[int, int]:
        """
        Return shortest distance from source user
        to every reachable user.
        """

        return self._bfs.distance_to_all(source_id)

    # =====================================================
    # Summary
    # =====================================================

    def summary(self) -> dict:
        """
        Return a summary of graph statistics.
        """

        largest_component = self._largest_component()

        user = self.most_connected_user()

        return {
            "total_users": self.total_users(),
            "total_relationships": self.total_relationships(),
            "average_friends": self.average_friends(),
            "largest_group_size": len(largest_component),
            "largest_group_members": largest_component,
            "most_connected_user": (
                None
                if user is None
                else {
                    "id": user.id,
                    "degree": self._graph.degree(user.id),
                }
            ),
        }