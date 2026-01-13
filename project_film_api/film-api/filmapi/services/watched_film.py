from typing import Iterable, Any

from pydantic import UUID4

from filmapi.repositories.iwatched_film import IWatchedFilmRepository
from filmapi.services.iwatched_film import IWatchedFilmService


class WatchedFilmService(IWatchedFilmService):
    """A class implementing the watched film service."""
    _repository: IWatchedFilmRepository

    def __init__(self, repository: IWatchedFilmRepository) -> None:
        """The initializer of the 'watched film service'.

        Args:
            repository (IWatchedFilmRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_watched_films(self, user_id: UUID4) -> Iterable[Any]:
        """Abstract for getting all of user's watched films from the database.

        Args:
            user_id (UUID4): User's id.

        Returns:
            Iterable[Any]: List of user's watched films.
        """

        return await self._repository.get_all_watched_films(user_id)

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

        return await self._repository.get_watched_film(user_id, film_id)


    async def get_film_reviews(
            self,
            film_id: int,
    ) -> Iterable[Any]:
        """Abstract for getting a film's reviews.

        Args:
            film_id (int): Film's id.

        Returns:
            Iterable[Any]: Film's reviews.
        """

        return await self._repository.get_film_reviews(film_id)

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

        return await self._repository.get_film_average_rating(film_id)

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

        return await self._repository.get_average_user_rating(user_id)

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

        return await self._repository.get_film_watched_number(film_id)

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

        return await self._repository.get_user_watched_number(user_id)

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

        return await self._repository.add_to_watched(user_id, film_id, rating, review)

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

        return await self._repository.update_watched(user_id, film_id, rating, review)

    async def delete_watched(
            self,
            user_id: UUID4,
            film_id: int) -> bool:
        """Abstract for deleting a watched film from an user's list.

        Args:
            user_id (UUID5): User's id.
            film_id (int): Film's id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_watched(user_id, film_id)