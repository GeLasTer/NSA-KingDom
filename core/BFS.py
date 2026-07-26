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

    # =====================================================
    # Raw BFS Traversal
    # =====================================================

    def traverse(self, source_id:int | str) -> list[int]:
        """
        Perform a raw BFS starting from source_id.
        Returns the list of reachable user ids in visit order.
        """

        self._graph._validate_users(source_id)

        visited: set[int] = {source_id}
        queue: deque[int] = deque([source_id])
        order: list[int] = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in self._graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    # =====================================================
    # Shortest Path (با نگهداری parent برای بازسازی مسیر)
    # =====================================================

    def shortest_path(
            self, source_id:int | str, destination_id: int | str
    ) -> list[User] | None:
        """
        Find the shortest path between source_id and destination_id.
        Returns a list of User objects representing the path
        (from source to destination), or None if unreachable.
        """

        self._graph._validate_users(source_id, destination_id)

        if source_id == destination_id:
            return [self._graph.get_user(source_id)]

        visited: set[int] = {source_id}
        queue: deque[int] = deque([source_id])
        parent: dict[int, int] = {}

        while queue:
            current = queue.popleft()

            for neighbor in self._graph.get_neighbors(current):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                parent[neighbor] = current

                if neighbor == destination_id:
                    return self._reconstruct_path(parent, source_id, destination_id)

                queue.append(neighbor)

        # هیچ مسیری بین این دو کاربر وجود نداره
        return None

    def _reconstruct_path(
            self, parent: dict[int, int], source_id: int | str, destination_id: int | str
    ) -> list[User]:
        """
        Rebuild the actual path from source to destination
        using the parent map collected during BFS.
        """

        path_ids: list[int] = [destination_id]

        while path_ids[-1] != source_id:
            path_ids.append(parent[path_ids[-1]])

        path_ids.reverse()

        return [self._graph.get_user(user_id) for user_id in path_ids]

    # =====================================================
    # Distance To All
    # =====================================================

    def distance_to_all(self, source_id:int | str) -> dict[int, int]:
        """
        Compute the distance (number of edges) from source_id
        to every other reachable user.
        Returns a dict of user_id -> distance (source itself excluded).
        """

        self._graph._validate_users(source_id)

        visited: set[int] = {source_id}
        queue: deque[int] = deque([source_id])
        distance: dict[int, int] = {}

        while queue:
            current = queue.popleft()

            for neighbor in self._graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance[neighbor] = distance.get(current, 0) + 1
                    queue.append(neighbor)

        return distance

    # =====================================================
    # Display Helpers (تبدیل خروجی خام به فرمت خوانا)
    # =====================================================

    @staticmethod
    def _display_name(user: User) -> str:
        """Pick the best available label for a user (name > username > id)."""

        return getattr(user, "name", None) or getattr(user, "username", None) or str(user.id)

    def format_path(self, path: list[User] | None) -> str:
        """
        Format a path (list of User) as: 'Ali -> Sara -> Reza -> King'
        """

        if path is None:
            return "مسیری بین این دو کاربر پیدا نشد."

        return " -> ".join(self._display_name(user) for user in path)

    def format_distances(self, distances: dict[int, int]) -> dict[str, int]:
        """
        Convert a {user_id: distance} dict into a {user_name: distance} dict
        for display purposes, e.g. {"Sara": 1, "Reza": 1, "King": 2}
        """

        return {
            self._display_name(self._graph.get_user(user_id)): dist
            for user_id, dist in distances.items()
        }