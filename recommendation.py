"""
Friend recommendation algorithms.
"""

from __future__ import annotations

from core.graph import Graph
from core.exceptions import UserNotFound
from models.user import User


class Recommendation:
    """
    Friend recommendation system based on mutual friends.
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    # =====================================================

    def recommend(
        self,
        user_id: int,
        limit: int = 5
    ) -> list[tuple[User, int]]:
     pass 