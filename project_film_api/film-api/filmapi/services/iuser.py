"""A module containing user service."""


from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from filmapi.domain.user import UserIn
from filmapi.dto.userdto import UserDTO
from filmapi.dto.tokendto import TokenDTO


class IUserService(ABC):
    """An abstract class for user service."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> UserDTO | None:
        """A method registering a new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def follow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method following another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def unfollow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method unfollowing another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_followers(self, user_id: UUID4) -> Iterable[UserDTO]:
        """The method getting all followers of the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All followers of the user.
        """

    @abstractmethod
    async def get_following(self, user_id: UUID4) -> Iterable[UserDTO]:
        """The method getting all users followed by the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All users followed by the user.
        """

    @abstractmethod
    async def is_following(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method checking if the user is following another given user.

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Whether the user is following another given user.
        """