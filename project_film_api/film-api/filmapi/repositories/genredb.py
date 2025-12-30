from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from filmapi.domain.film import Film
from filmapi.repositories.igenre import IGenreRepository
from filmapi.domain.genre import Genre, GenreIn
from filmapi.db import (
    genre_table,
    film_table,
    film_genre_table,
    database, director_table,
)

class GenreRepository(IGenreRepository):
    async def get_all_genres(self) -> Iterable[Any]:
        """The method for getting all genres from the database.

                Returns:
                    Iterable[Any]: The collection of the all genres.
                """
        query = (genre_table.select()
                 .order_by(genre_table.c.name.asc()))
        genres = await database.fetch_all(query)
        return [Genre(**genre) for genre in genres]
    
    async def get_genre_by_name(self, name: str) -> Iterable[Any]:
        """The method for getting genres by a part of their name.
            Args:
                name (str): Part of genre's name.
            Returns:
                Iterable[Any]: The collection of genres that match.
                """
        query = (genre_table.select()
                 .where(genre_table.c.name.ilike(f'%{name}%'))
                 .order_by(genre_table.c.name.asc()))
        genres = await database.fetch_all(query)
        return [Genre(**dict(genre)) for genre in genres]

    async def get_by_id(self, genre_id: int) -> Any | None:
        """The method for getting a genre by its id.
            Args:
                genre_id (int): Genre's id.
            Returns:
                Any | None: Genre from the database."""

        genre = await self._get_by_id(genre_id)
        return Genre(**dict(genre)) if genre else None

    async def create_genre(self, data: GenreIn) -> Any | None:
        """The method for creating a new genre in database.
            Args:
                data (GenreIn): Attributes of the genre.
            Returns:
                Any | None: Newly created genre. """
        query = (genre_table.insert()
                 .values(**data.model_dump()))
        new_genre_id = await database.execute(query)
        new_genre = await self._get_by_id(new_genre_id)
        return Genre(**dict(new_genre)) if new_genre else None

    async def edit_genre(self, genre_id: int, data: GenreIn) -> Any | None:
        """The method for updating genre data in database.
            Args:
                genre_id (int): Genre's id.
                data (GenreIn): New attributes for the genre.
            Returns:
                Any | None: Updated genre. """

        if await self._get_by_id(genre_id):
            query = (
                genre_table.update()
                .where(genre_table.c.id == genre_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            genre = await self._get_by_id(genre_id)
            return Genre(**dict(genre)) if genre else None
        return None

    async def delete_genre(self, genre_id: int) -> bool:
        """The method for deleting a genre from the database.
            Args:
                genre_id (int): Genre's id.
            Returns:
                bool: Operation's success."""
        if await self._get_by_id(genre_id):
            query = genre_table \
                .delete() \
                .where(genre_table.c.id == genre_id)
            await database.execute(query)

            return True
        return False

    async def _get_by_id(self, genre_id: int) -> Record | None:
        """A private method for getting a genre from the db by its ID.
            Args:
                genre_id (int): Genre's id.
            Returns:
                Any | None: Genre record if possible."""
        query = (genre_table.select()
                 .where(genre_table.c.id == genre_id))
        return await database.fetch_one(query)