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
            {"id": user.id, "name": user.name} for user in graph.get_users()
        ]

        seen: set[frozenset] = set()
        edges_data = []
        for user_id in graph.user_ids():
            for neighbor_id in graph.get_neighbors(user_id):
                pair = frozenset((user_id, neighbor_id))
                if pair not in seen:
                    seen.add(pair)
                    edges_data.append([user_id, neighbor_id])

        data = {"users": users_data, "edges": edges_data}

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(filepath: str | Path) -> Graph:
        
        filepath = Path(filepath)
        with filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)

        graph = Graph()

        for user_data in data.get("users", []):
            user = User(id=user_data["id"], name=user_data["name"])
            try:
                graph.add_user(user)
            except DuplicateUser:
               
                continue

        for source_id, target_id in data.get("edges", []):
            try:
                graph.add_edge(source_id, target_id)
            except (DuplicateEdge, UserNotFound):
                continue

        return graph

    @staticmethod
    def validate_schema(filepath: str | Path) -> bool:
        
        try:
            filepath = Path(filepath)
            with filepath.open("r", encoding="utf-8") as f:
                data = json.load(f)

            if "users" not in data or "edges" not in data:
                return False

            user_ids = set()
            for user in data["users"]:
                if "id" not in user or "name" not in user:
                    return False
                user_ids.add(user["id"])

            for edge in data["edges"]:
                if len(edge) != 2:
                    return False
                if edge[0] not in user_ids or edge[1] not in user_ids:
                    return False

            return True
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return False
