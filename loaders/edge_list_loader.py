"""
Load graph data from a plain-text edge-list file.

Expected file format (one edge per line):
    source target weight
Example:
    Y O2 1
    O2 Z2 1

Note: `weight` is currently ignored because Graph is unweighted.
"""

from __future__ import annotations

from pathlib import Path

from core.graph import Graph
from core.exceptions import DuplicateEdge
from models.user import User


class EdgeListLoader:

    def load(self, path: str | Path) -> Graph:
        graph = Graph()
        path = Path(path)

        skipped_duplicates = 0
        skipped_self_loops = 0

        with path.open("r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                parts = line.split()
                if len(parts) < 2:
                    continue  # invalid line, skip

                source_id, target_id = parts[0], parts[1]
                # weight = float(parts[2]) if len(parts) > 2 else 1.0  # currently unused

                if source_id == target_id:
                    skipped_self_loops += 1
                    continue

                if not graph.has_user(source_id):
                    graph.add_user(User(id=source_id, name=source_id))

                if not graph.has_user(target_id):
                    graph.add_user(User(id=target_id, name=target_id))

                try:
                    graph.add_edge(source_id, target_id)
                except DuplicateEdge:
                    skipped_duplicates += 1
                    continue

        print(f"Loaded graph: {graph.node_count()} users, {graph.edge_count()} edges")
        print(f"Skipped duplicates: {skipped_duplicates}, self-loops: {skipped_self_loops}")

        return graph