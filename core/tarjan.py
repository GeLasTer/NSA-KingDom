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

        pass