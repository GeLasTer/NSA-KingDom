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
        user_id: int | str,
        limit: int = 5
    ) -> list[tuple[User, int]]:
        """
        Recommend users based on the number
        of mutual friends.
        """

        if not self.graph.has_user(user_id):
            raise UserNotFound(
                f"User {user_id} does not exist."
            )

        friends = self.graph.get_neighbors(user_id)

        scores: dict[int, int] = {}

        for friend in friends:

            for candidate in self.graph.get_neighbors(friend):

                if candidate == user_id:
                    continue

                if candidate in friends:
                    continue

                scores[candidate] = (
                    scores.get(candidate, 0) + 1
                )

        ranked = sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0])
        )

        result = []

        for candidate_id, score in ranked[:limit]:

            result.append(
                (
                    self.graph.get_user(candidate_id),
                    score
                )
            )

        return result