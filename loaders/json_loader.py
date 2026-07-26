"""
Load graph data from JSON files.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.graph import Graph
from models.user import User

class JsonLoader:
    """
    Responsible for loading users and relationships
    from JSON files into a Graph.
    """

    def load(self,
             users_path: str | Path,
             relationships_path: str | Path
             ) -> Graph:

        graph = Graph()

        self.load_users(graph, users_path)
        self.load_relationships(graph, relationships_path)

        return graph

    # ==================================================

    def load_users(self,
                   graph: Graph,
                   users_path: str | Path
                   ) -> None:

        path = Path(users_path)

        with path.open("r", encoding="utf-8") as file:
            users = json.load(file)

        for user_data in users:

            user = User.from_dict(user_data)

            graph.add_user(user)

    # ==================================================

    def load_relationships(self,
                           graph: Graph,
                           relationships_path: str | Path
                           ) -> None:

        path = Path(relationships_path)

        with path.open("r", encoding="utf-8") as file:
            relationships = json.load(file)

        for relation in relationships:

            # Example:
            # {
            #   "source": 1,
            #   "target": 5
            # }

            graph.add_edge(
                relation["source"],
                relation["target"]
            )