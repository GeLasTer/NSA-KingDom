"""
Tarjan algorithm implementation for the NSA Kingdom Project.
"""


class Tarjan:
    """
    Finds:
        - Bridges
        - Articulation Points
    """

    def __init__(self, graph):
        self.graph = graph

        self.visited = {}
        self.discovery_time = {}
        self.low = {}
        self.parent = {}

        self.time = 0

        self.bridges = []
        self.articulation_points = set()

    def run(self):
        """
        Run Tarjan algorithm on the entire graph.
        """

        for user_id in self.graph.user_ids():

            if user_id not in self.visited:

                self.parent[user_id] = None
                self._dfs(user_id)

    def _dfs(self, user_id):
        """
        Tarjan DFS algorithm.
        """

        self.visited[user_id] = True

        self.discovery_time[user_id] = self.time
        self.low[user_id] = self.time

        self.time += 1

        children = 0

        for neighbor in self.graph.get_neighbors(user_id):

            if neighbor not in self.visited:

                self.parent[neighbor] = user_id
                children += 1

                self._dfs(neighbor)

                self.low[user_id] = min(
                    self.low[user_id],
                    self.low[neighbor]
                )

                # Bridge
                if self.low[neighbor] > self.discovery_time[user_id]:
                    self.bridges.append((user_id, neighbor))

                # Articulation Point (root)
                if (
                    self.parent[user_id] is None
                    and children > 1
                ):
                    self.articulation_points.add(user_id)

                # Articulation Point (non-root)
                if (
                    self.parent[user_id] is not None
                    and self.low[neighbor] >= self.discovery_time[user_id]
                ):
                    self.articulation_points.add(user_id)

            elif neighbor != self.parent.get(user_id):

                self.low[user_id] = min(
                    self.low[user_id],
                    self.discovery_time[neighbor]
                )