from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4


class IWatchedFilmService(ABC):
    @abstractmethod
    async def get_all_watched_films(self, user_id: UUID4) -> Iterable[Any]:
        """Abstract for getting all of user's watched films from the database.

        Args:
            user_id (UUID4): User's id.

        Returns:
            Iterable[Any]: List of user's watched films.
        """

    @abstractmethod
    async def get_watched_film(
            self,
            user_id: UUID4,
            film_id: int,
    ) -> Any | None:
        """Abstract for getting user's specific watched film from the database.

        Args:
            user_id (UUID4): User's id.
            film_id (int): Film's id.

        Returns:
            Any | None: User's watched film if it exists.
        """

    @abstractmethod
    async def get_film_reviews(
            self,
            film_id: int,
    ) -> Iterable[Any]:
        """Abstract for getting a film's reviews.

        Args:
            film_id (UUID5): Film's id.

        Returns:
            Iterable[Any]: Film's reviews.
        """

    @abstractmethod
    async def get_user_reviews(
            self,
            user_id: UUID4,
    ) -> Iterable[Any]:
        """Abstract for getting a user's reviews.

        Args:
            user_id (UUID4): User's id.

        Returns:
            Iterable[Any]: User's reviews.
        """

    @abstractmethod
    async def get_recent_followed_reviews(
            self,
            user_id: UUID4,
            limit: int,
    ) -> Iterable[Any]:
        """Abstract for getting recent reviews from users the given user follows.

        Args:
            user_id (UUID4): User's id.
            limit (int): Number of reviews to return.

        Returns:
            Iterable[Any]: List of reviews
        """

    @abstractmethod
    async def get_film_average_rating(
            self,
            film_id: int,
    ) -> float:
        """Abstract for getting a film's average rating.

        Args:
            film_id (int): Film's id.

        Returns:
            float: Film's average rating.
        """

    @abstractmethod
    async def get_average_user_rating(
            self,
            user_id: UUID4,
    ) -> float:
        """Abstract for getting an user's average film rating.

        Args:
            user_id (UUID4): User's id.

        Returns:
            float: User's average film rating.
        """

    @abstractmethod
    async def get_film_watched_number(
            self,
            film_id: int
    ) -> int:
        """Abstract for getting the number of users that watched a given film.

        Args:
            film_id (int): Film's id.

        Returns:
            int: Number of users that watched a given film.
        """

    @abstractmethod
    async def get_user_watched_number(
            self,
            user_id: UUID4
    ) -> int:
        """Abstract for getting the number of films watched by given user.

        Args:
            user_id (UUID4): User's id.

        Returns:
            int: Number of films watched by a given user.
        """

    @abstractmethod
    async def add_to_watched(
            self,
            user_id: UUID4,
            film_id: int,
            rating: int | None = None,
            review: str | None = None,
            ) -> Any | None:
        """Abstract for adding a film to an user's watched list.

        Args:
            user_id (UUID4): User's id.
            film_id (int): Added film's id.
            rating (int): Rating given to the film (1-10).
            review (str): Review's text.

        Returns:
            Any | None: Added film.
        """

    @abstractmethod
    async def update_watched(
            self,
            user_id: UUID4,
            film_id: int,
            rating: int | None = None,
            review: str | None = None,
            ) -> Any | None:
        """Abstract for editing a user's watched film.

        Args:
            user_id (UUID4): User's id.
            film_id (int): Film's id.
            rating (int): Rating given to the film (1-10).
            review (str): Review's text.

        Returns:
            Any | None: Added film.
        """

    @abstractmethod
    async def delete_watched(
            self,
            user_id: UUID4,
            film_id: int) -> bool:
        """Abstract for deleting a watched film from an user's list.

        Args:
            user_id (UUID4): User's id.
            film_id (int): Film's id.

        Returns:
            bool: Success of the operation.
        """