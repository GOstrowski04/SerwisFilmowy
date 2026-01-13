"""A module containing user service."""
from typing import Iterable

from pydantic import UUID4

from filmapi.domain.user import UserIn
from filmapi.repositories.iuser import IUserRepository
from filmapi.dto.userdto import UserDTO
from filmapi.dto.tokendto import TokenDTO
from filmapi.services.iuser import IUserService
from filmapi.utils.password import verify_password
from filmapi.utils.token import generate_user_token


class UserService(IUserService):
    """An abstract class for user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:
        """A method registering a new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

        return await self._repository.register_user(user)

    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

        if user_data := await self._repository.get_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(user_data.id)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self._repository.get_by_uuid(uuid)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self._repository.get_by_email(email)

    async def follow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method following another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.follow_user(follower_id, followed_id)

    async def unfollow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method unfollowing another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.unfollow_user(follower_id, followed_id)

    async def get_followers(self, user_id: UUID4) -> Iterable[UserDTO]:
        """The method getting all followers of the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All followers of the user.
        """

        return await self._repository.get_followers(user_id)

    async def get_following(self, user_id: UUID4) -> Iterable[UserDTO]:
        """The method getting all users followed by the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All users followed by the user.
        """

        return await self._repository.get_following(user_id)

    async def is_following(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """The method checking if the user is following another given user.

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Whether the user is following another given user.
        """

        return await self._repository.is_following(follower_id, followed_id)