from __future__ import annotations

import json
from pathlib import Path

from models.user import User
from core.graph import Graph
from core.exceptions import DuplicateUser, DuplicateEdge, UserNotFound


class GraphStorage:

    @staticmethod
    def save(graph: Graph, filepath: str | Path) -> None:
        # همان کد Commit 2
        ...


    @staticmethod
    def load(filepath: str | Path) -> Graph:

        filepath = Path(filepath)

        with filepath.open(
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        graph = Graph()

        for user_data in data.get("users", []):

            user = User(
                id=user_data["id"],
                name=user_data["name"]
            )

            try:
                graph.add_user(user)

            except DuplicateUser:
                continue


        for source_id, target_id in data.get("edges", []):

            try:
                graph.add_edge(
                    source_id,
                    target_id
                )

            except (DuplicateEdge, UserNotFound):
                continue

        return graph


    @staticmethod
    def validate_schema(filepath: str | Path) -> bool:
        pass