"""A repository for user entity."""


from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from filmapi.domain.user import UserIn
from filmapi.dto.userdto import UserDTO


class IUserRepository(ABC):
    """An abstract repository class for user."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """An abstract registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """An abstract getting user by UUID.

        Args:
            uuid (UUID4): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """An abstract getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def follow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """An abstract following another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def unfollow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """An abstract unfollowing another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_followers(self, user_id: UUID4) -> Iterable[UserDTO]:
        """An abstract getting all followers of the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All followers of the user.
        """

    @abstractmethod
    async def get_following(self, user_id: UUID4) -> Iterable[UserDTO]:
        """An abstract getting all users followed by the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All users followed by the user.
        """

    @abstractmethod
    async def is_following(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """An abstract checking if the user is following another given user.

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Whether the user is following another given user.
        """