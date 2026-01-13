"""A repository for user entity."""


from typing import Any, Iterable

from pydantic import UUID4
from sqlalchemy import select

from filmapi.dto.userdto import UserDTO
from filmapi.utils.password import hash_password
from filmapi.domain.user import UserIn
from filmapi.repositories.iuser import IUserRepository
from filmapi.db import database, user_table, follow_table


class UserRepository(IUserRepository):
    """An implementation of repository class for user."""

    async def register_user(self, user: UserIn) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        query = user_table.insert().values(**user.model_dump())
        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.id == uuid)
        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.email == email)
        user = await database.fetch_one(query)

        return user

    async def follow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """A method following another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """

        query = (
            follow_table.insert()
            .values(follower_id=follower_id, followed_id=followed_id)
        )
        await database.execute(query)
        return True

    async def unfollow_user(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """A method unfollowing another user

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
         """

        query = (
            follow_table.delete()
            .where(
                follow_table.c.follower_id == follower_id,
                follow_table.c.followed_id == followed_id,
            )
        )
        await database.execute(query)
        return True

    async def get_followers(self, user_id: UUID4) -> Iterable[UserDTO]:
        """A method getting all followers of the user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All followers of the user.
        """

        query = (
            select(
                user_table.c.id,
                user_table.c.email,
            ).select_from(
                follow_table
                .join(user_table, user_table.c.id == follow_table.c.follower_id)
            ).where(
                follow_table.c.followed_id == user_id
            )
        )
        followers = await database.fetch_all(query)
        return [UserDTO(**user) for user in followers]

    async def get_following(self, user_id: UUID4) -> Iterable[UserDTO]:
        """A method getting all followed users by given user.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserDTO]: All followed users by the user.
        """

        query = (
            select(
                user_table.c.id,
                user_table.c.email,
            ).select_from(
                follow_table
                .join(user_table, user_table.c.id == follow_table.c.followed_id)
            ).where(
                follow_table.c.follower_id == user_id
            )
        )
        followed = await database.fetch_all(query)
        return [UserDTO(**user) for user in followed]

    async def is_following(self, follower_id: UUID4, followed_id: UUID4) -> bool:
        """A method checking if the user is following another given user.

        Args:
            follower_id (UUID4): The user id.
            followed_id (UUID4): The user id.

        Returns:
             bool: Whether the user is following another given user.
        """

        query = (
            select(follow_table.c.follower_id)
            .where(
                follow_table.c.follower_id == follower_id,
                follow_table.c.followed_id == followed_id,
            )
        )
        follower = await database.fetch_one(query)
        return follower is not None