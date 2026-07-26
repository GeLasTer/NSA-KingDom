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

        elif neighbor != self.parent.get(user_id):

            self.low[user_id] = min(
                self.low[user_id],
                self.discovery_time[neighbor]
            )