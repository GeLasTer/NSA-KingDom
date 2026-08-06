"""
Detects the dataset type from file extension/content and
returns a Graph, regardless of the underlying format.
"""

from __future__ import annotations

from pathlib import Path

from core.graph import Graph
from loaders.json_loader import JsonLoader
from loaders.edge_list_loader import EdgeListLoader


class LoaderFactory:

    @staticmethod
    def load(path: str | Path, relationships_path: str | Path | None = None) -> Graph:
        """
        Auto-detect and load a dataset.

        Usage:
            # single edge-list / csv / txt file:
            LoaderFactory.load("data/edges.txt")

            # split JSON (users file + relationships file):
            LoaderFactory.load("data/users.json", "data/relationships.json")
        """

        path = Path(path)
        suffix = path.suffix.lower()

        if suffix == ".json":
            if relationships_path is None:
                raise ValueError(
                    "JSON datasets require both a users file and a "
                    "relationships file. Pass relationships_path=..."
                )
            return JsonLoader().load(path, relationships_path)

        if suffix in (".txt", ".csv", ".tsv"):
            return EdgeListLoader().load(path)

        raise ValueError(f"Unsupported dataset format: '{suffix}'")