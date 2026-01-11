
from datetime import datetime
from typing import Any, Iterable

from asyncpg import Record
from pydantic import UUID5
from sqlalchemy import select

from filmapi.domain.watched_film import WatchedFilm
from filmapi.dto.watched_filmdto import WatchedFilmDTO, ReviewDTO
from filmapi.repositories.iwatched_film import IWatchedFilmRepository
from filmapi.db import (
    watched_films_table,
    film_table,
    database,
)

class WatchedFilmRepository(IWatchedFilmRepository):
    async def get_all_watched_films(self, user_id: UUID5) -> Iterable[Any]:
        """The method for getting all of user's watched films from the database.
        Args:
            user_id (UUID5): User's id.

        Returns:
            Iterable[WatchedFilm]: List of user's watched films."""
        query = (
            select(
                watched_films_table.c.film_id,
                film_table.c.title,
                watched_films_table.c.rating,
            )
            .select_from(
                watched_films_table
                .join(film_table, watched_films_table.c.film_id == film_table.c.id)
            )
            .where(watched_films_table.c.user_id == user_id)
        )
        watched_films = await database.fetch_all(query)
        return [WatchedFilmDTO.from_record(film) for film in watched_films]

    async def get_watched_film(
            self,
            user_id: UUID5,
            film_id: int,
    ) -> Any | None:
        """The method for getting an user's specific watched film from the database.
        Args:
            user_id (UUID5): User's id.
            film_id (int): Film's id.

        Returns:
            Any | None: User's watched film if it exists."""
        query = (
            select(
                watched_films_table.c.film_id,
                film_table.c.title,
                watched_films_table.c.rating,
            )
            .select_from(
                watched_films_table
                .join(film_table, watched_films_table.c.film_id == film_table.c.id)
            )
            .where(
                watched_films_table.c.user_id == user_id,
                watched_films_table.c.film_id == film_id,
            )
        )
        watched_film = await database.fetch_one(query)
        return WatchedFilmDTO.from_record(watched_film) if watched_film else None


    async def get_film_reviews(
            self,
            film_id: int,
    ) -> Iterable[Any]:
        """The method for getting a film's reviews.
        Args:
            film_id (UUID5): Film's id.

        Returns:
            Iterable[Any]: Film's reviews."""
        query = (
            select(
                watched_films_table.user_id,
                film_table.c.title,
                watched_films_table.c.rating,
                watched_films_table.c.review,
                watched_films_table.c.review_date,
            )
            .select_from(
                watched_films_table
                .join(film_table, watched_films_table.c.film_id == film_table.c.id)
            )
            .where(
                watched_films_table.c.film_id == film_id,
                watched_films_table.c.review.isnot(None),
            )
        )
        reviews = await database.fetch_all(query)
        return [ReviewDTO.from_record(review) for review in reviews]

    async def add_to_watched(
            self,
            user_id: UUID5,
            film_id: int,
            rating: int | None = None,
            review: str | None = None,
    ) -> Any | None:
        """Abstract for adding a film to an user's watched list.
        Args:
            user_id (UUID5): User's id.
            film_id (int): Added film's id.
            rating (int): Rating given to the film (1-10).
            review (str): Review's text.

        Returns:
            Any | None: Added film."""
        test = await self.get_watched_film(film_id=film_id, user_id=user_id)
        if test:
            return test
        query = (watched_films_table.insert()
                 .values(user_id=user_id,
                         film_id=film_id,
                         rating=rating,
                         review=review,
                         review_date=datetime.now())
                 )
        await database.execute(query)
        return await self.get_watched_film(film_id=film_id, user_id=user_id)

    async def update_watched(
            self,
            user_id: UUID5,
            film_id: int,
            rating: int | None = None,
            review: str | None = None,
    ) -> Any | None:
        """Abstract for editing a user's watched film.
        Args:
            user_id (UUID5): User's id.
            film_id (int): Film's id.
            rating (int): Rating given to the film (1-10).
            review (str): Review's text.

        Returns:
            Any | None: Updated film."""
        if await self._get_by_id(film_id=film_id, user_id=user_id):
            query = (
                watched_films_table.update()
                .where(
                watched_films_table.c.user_id == user_id,
                watched_films_table.c.film_id == film_id
                )
                .values(user_id=user_id,
                        film_id=film_id,
                        rating=rating,
                        review=review,
                        review_date=datetime.now())
                )
            await database.execute(query)
            return await self.get_watched_film(film_id=film_id, user_id=user_id)
        return None

    async def delete_watched(
            self,
            user_id: UUID5,
            film_id: int) -> bool:
        """Abstract for deleting a watched film from an user's list.
        Args:
            user_id (UUID5): User's id.
            film_id (int): Film's id.

        Returns:
            bool: Success of the operation."""
        if await self._get_by_id(user_id=user_id, film_id=film_id):
            query = (watched_films_table.delete()
                     .where(watched_films_table.c.film_id == film_id,
                            watched_films_table.c.user_id == user_id
                            ))
            await database.execute(query)
            return True
        return False


    async def _get_by_id(self, film_id: int, user_id: UUID5) -> Record | None:
        """A private method for getting a watched film from the db by its IDs.
            Args:
                film_id (int): Film's id.
                user_id (UUID5): User's id.
            Returns:
                Any | None: Film record if possible."""
        query = (watched_films_table.select()
                 .where(
            watched_films_table.c.film_id == film_id,
            watched_films_table.c.user_id == user_id))
        return await database.fetch_one(query)