from __future__ import annotations

import json
from pathlib import Path

from models.user import User
from core.graph import Graph
from core.exceptions import DuplicateUser, DuplicateEdge, UserNotFound


class GraphStorage:

    @staticmethod
    def save(graph: Graph, filepath: str | Path) -> None:
        pass

    @staticmethod
    def load(filepath: str | Path) -> Graph:
        pass

    @staticmethod
    def validate_schema(filepath: str | Path) -> bool:
        pass