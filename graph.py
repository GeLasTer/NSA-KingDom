"""
Graph implementation for the NSA Kingdom Project.
"""

from __future__ import annotations

from models.user import User
from core.exceptions import (
    DuplicateUser,
    UserNotFound,
    DuplicateEdge,
    InvalidEdge,
)


class Graph:
    """
    Represents an undirected graph.

    Users are stored as:
        id -> User

    Friendships are stored as:
        id -> set(friend_ids)
    """

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._adjacency: dict[int, set[int]] = {}

    # =====================================================
    # User Methods
    # =====================================================

    def add_user(self, user: User) -> None:
        """Add a new user to the graph."""

        if user.id in self._users:
            raise DuplicateUser(f"User {user.id} already exists.")

        self._users[user.id] = user
        self._adjacency[user.id] = set()

    def remove_user(self, user_id: int) -> None:
        """Remove a user and all of their friendships."""

        self._validate_users(user_id)

        for friend_id in self._adjacency[user_id]:
            self._adjacency[friend_id].remove(user_id)

        del self._adjacency[user_id]
        del self._users[user_id]

    def get_user(self, user_id: int) -> User:
        """Return the User object."""

        self._validate_users(user_id)

        return self._users[user_id]

    def has_user(self, user_id: int) -> bool:
        """Check whether a user exists."""

        return user_id in self._users

    def get_users(self) -> list[User]:
        """Return all users."""

        return list(self._users.values())

    # =====================================================
    # Edge Methods
    # =====================================================

    def add_edge(self, source_id: int, target_id: int) -> None:
        """Create a friendship."""

        self._validate_users(first, second)

        if first == second:
            raise InvalidEdge("A user cannot connect to itself.")

        if second in self._adjacency[first]:
            raise DuplicateEdge("Friendship already exists.")

        self._adjacency[first].add(second)
        self._adjacency[second].add(first)

    def remove_edge(self, first: int, second: int) -> None:
        """Remove a friendship."""

        self._validate_users(first, second)

        self._adjacency[first].discard(second)
        self._adjacency[second].discard(first)

    def has_edge(self, first: int, second: int) -> bool:
        """Check if two users are connected."""

        self._validate_users(first, second)

        return second in self._adjacency[first]

    def get_neighbors(self, user_id: int) -> set[int]:
        """Return neighbors of a user."""

        self._validate_users(user_id)

        return self._adjacency[user_id].copy()

    def degree(self, user_id: int) -> int:
        """Return number of friendships."""

        self._validate_users(user_id)

        return len(self._adjacency[user_id])

    # =====================================================
    # Statistics
    # =====================================================

    def node_count(self) -> int:
        """Return number of users."""

        return len(self._users)

    def edge_count(self) -> int:
        """Return number of friendships."""

        total = sum(len(neighbors) for neighbors in self._adjacency.values())

        return total // 2

    # =====================================================
    # Utility
    # =====================================================

    def clear(self) -> None:
        """Remove everything from the graph."""

        self._users.clear()
        self._adjacency.clear()

    def _validate_users(self, *user_ids: int) -> None:
        """Validate that all given users exist."""

        for user_id in user_ids:
            if user_id not in self._users:
                raise UserNotFound(f"User {user_id} does not exist.")

    # =====================================================
    # Magic Methods
    # =====================================================

    def __contains__(self, user_id: int) -> bool:
        return user_id in self._users

    def __len__(self) -> int:
        return self.node_count()

    def __str__(self) -> str:
        lines = []

        for user_id in sorted(self._users):
            neighbors = sorted(self._adjacency[user_id])
            lines.append(f"{user_id} -> {neighbors}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Graph(users={self.node_count()}, "
            f"edges={self.edge_count()})"
        )
    def users(self) -> list[User]:
        return list(self._users.values())

    def user_ids(self) -> list[int]:
         return list(self._users.keys())