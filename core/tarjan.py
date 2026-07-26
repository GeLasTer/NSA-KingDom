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