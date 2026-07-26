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
"""
    # ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from core.graph import Graph
    from models.user import User

    # ساخت یک گراف نمونه
    graph = Graph()

    # اضافه کردن کاربران
    users = [
        (1, "Ali"),
        (2, "Sara"),
        (3, "Reza"),
        (4, "King"),
        (5, "Minister"),
        (6, "Spy"),
    ]

    for uid, name in users:
        graph.add_user(User(id=uid, name=name))

    # اضافه کردن روابط
    graph.add_edge(1, 2)  # Ali - Sara
    graph.add_edge(2, 3)  # Sara - Reza
    graph.add_edge(3, 4)  # Reza - King
    graph.add_edge(4, 5)  # King - Minister

    # کامپوننت دوم
    graph.add_edge(6, 5)  # Spy - Minister

    # ساخت شی Statistics
    stats = Statistics(graph)

    print("=" * 50)
    print("Statistics Test")
    print("=" * 50)

    print(f"Total Users: {stats.total_users()}")
    print(f"Total Relationships: {stats.total_relationships()}")
    print(f"Average Friends: {stats.average_friends():.2f}")

    user = stats.most_connected_user()
    if user:
        name = getattr(user, "name", None) or getattr(user, "username", None) or str(user.id)
        print(f"Most Connected User: {name} (ID={user.id})")
        print(f"Degree: {graph.degree(user.id)}")

    print(f"Largest Group Size: {stats.largest_group_size()}")

    print("Largest Group Members:")
    for member in stats.largest_group_members():
        name = getattr(member, "name", None) or getattr(member, "username", None) or str(member.id)
        print(f"  - {name} (ID={member.id})")

    print("\nDistance Analysis From Ali:")
    distances = stats.distance_analysis(1)

    for user_id, distance in distances.items():
        user = graph.get_user(user_id)
        name = getattr(user, "name", None) or getattr(user, "username", None) or str(user.id)
        print(f"  {name}: {distance}")

    print("\nSummary:")
    print(stats.summary())
"""