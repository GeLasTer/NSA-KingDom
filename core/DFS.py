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

    # =====================================================
    # Simple DFS Traversal (Iterative با Stack صریح)
    # =====================================================

    def traverse(self, start_id: int) -> list[int]:
        """
        Perform a simple iterative DFS starting from start_id.
        Returns the list of reachable user ids in visit order.
        """

        self._graph._validate_users(start_id)

        visited: set[int] = set()
        stack: list[int] = [start_id]
        order: list[int] = []

        while stack:
            current = stack.pop()

            # این چک برای جلوگیری از حلقه (Loop) لازمه:
            # ممکنه یک نود چند بار قبل از visit شدن، توی stack قرار بگیره
            if current in visited:
                continue

            visited.add(current)
            order.append(current)

            # ترتیب معکوس تا خروجی شبیه DFS بازگشتی معمولی باشه
            # (کوچیک‌ترین id اول pop بشه)
            neighbors = sorted(self._graph.get_neighbors(current), reverse=True)

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

        return order

    # =====================================================
    # Connected Components
    # =====================================================

    def connected_components(self) -> list[list[int]]:
        """
        Find all connected components in the graph.
        Returns a list of components, where each component is
        a list of user ids belonging to the same connected group.
        """

        visited: set[int] = set()
        components: list[list[int]] = []

        for node_id in self._graph.user_ids():
            if node_id not in visited:
                component = self.traverse(node_id)
                visited.update(component)
                components.append(component)

        return components

    # =====================================================
    # Display Helpers (تبدیل خروجی خام به فرمت خوانا)
    # =====================================================

    @staticmethod
    def _display_name(user: User) -> str:
        """Pick the best available label for a user (name > username > id)."""

        return getattr(user, "name", None) or getattr(user, "username", None) or str(user.id)

    def format_traverse(self, order: list[int]) -> str:
        """
        Format a traversal order as: 'Ali -> Sara -> Reza -> King'
        """

        return " -> ".join(
            self._display_name(self._graph.get_user(user_id)) for user_id in order
        )

    def format_components(self, components: list[list[int]]) -> list[list[str]]:
        """
        Convert components (list of id-lists) into name-based lists
        for display purposes.
        """

        return [
            [self._display_name(self._graph.get_user(user_id)) for user_id in component]
            for component in components
        ]


# ==========================================
# تست کد
# ==========================================
# if __name__ == "__main__":
#     from core.graph import Graph
#     from models.user import User
#
#     graph = Graph()
#
#     # کامپوننت اول: Ali - Sara - Reza - King
#     for uid, name in [(1, "Ali"), (2, "Sara"), (3, "Reza"), (4, "King")]:
#         graph.add_user(User(id=uid, name=name))
#
#     graph.add_edge(1, 2)
#     graph.add_edge(2, 3)
#     graph.add_edge(3, 4)
#
#     # کامپوننت دوم: جدا از بقیه (Minister - Spy)
#     graph.add_user(User(id=5, name="Minister"))
#     graph.add_user(User(id=6, name="Spy"))
#     graph.add_edge(5, 6)
#
#     dfs = DFS(graph)
#
#     print("--- Traverse (from Ali) ---")
#     order = dfs.traverse(1)
#     print(dfs.format_traverse(order))
#
#     print("\n--- Connected Components ---")
#     components = dfs.connected_components()
#     print(dfs.format_components(components))