from __future__ import annotations

import json
from pathlib import Path

from models.user import User
from core.graph import Graph
from core.exceptions import DuplicateUser, DuplicateEdge, UserNotFound


class GraphStorage:

    @staticmethod
    def save(graph: Graph, filepath: str | Path) -> None:

        users_data = [
            {"id": user.id, "name": user.name}
            for user in graph.get_users()
        ]

        seen: set[frozenset] = set()
        edges_data = []

        for user_id in graph.user_ids():
            for neighbor_id in graph.get_neighbors(user_id):

                pair = frozenset((user_id, neighbor_id))

                if pair not in seen:
                    seen.add(pair)
                    edges_data.append(
                        [user_id, neighbor_id]
                    )

        data = {
            "users": users_data,
            "edges": edges_data
        }

        filepath = Path(filepath)
        filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

    @staticmethod
    def load(filepath: str | Path) -> Graph:
        pass

    @staticmethod
    def validate_schema(filepath: str | Path) -> bool:
        pass