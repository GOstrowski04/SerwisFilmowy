from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from filmapi.domain.film import Film
from filmapi.repositories.idirector import IDirectorRepository
from filmapi.domain.director import Director, DirectorIn
from filmapi.db import (
    director_table,
    database, film_table,
)

class DirectorRepository(IDirectorRepository):
    async def get_all_directors(self) -> Iterable[Any]:
        """The method for getting all directors from the database.

                Returns:
                    Iterable[Any]: The collection of the all directors.
                """
        query = (director_table.select()
                 .order_by(director_table.c.name.asc()))
        directors = await database.fetch_all(query)
        return [Director(**dict(director)) for director in directors]

    async def get_director_by_name(self, name: str) -> Iterable[Any]:
        """The method for getting directors by a part of their name.
            Args:
                name (str): Part of director's name.
            Returns:
                Iterable[Any]: The collection of directors that match.
                """
        query = (director_table.select()
                 .where(director_table.c.name.ilike(f'%{name}%'))
                 .order_by(director_table.c.name.asc()))
        directors = await database.fetch_all(query)
        return [Director(**dict(director)) for director in directors]

    async def get_director_by_id(self, director_id: int) -> Any | None:
        """The method for getting a director by its id.
            Args:
                director_id (int): Director's id.
            Returns:
                Any | None: Director from the database."""

        director = await self._get_by_id(director_id)
        return Director(**dict(director)) if director else None


    async def create_director(self, data: DirectorIn) -> Any | None:
        """The method for creating a new director in database.
            Args:
                data (DirectorIn): Attributes of the director.
            Returns:
                Any | None: Newly created director. """
        query = (director_table.insert()
                 .values(**data.model_dump()))
        new_director_id = await database.execute(query)
        new_director = await self._get_by_id(new_director_id)
        return Director(**dict(new_director)) if new_director else None

    async def edit_director(self, director_id: int, data: DirectorIn) -> Any | None:
        """The method for updating director data in database.
            Args:
                director_id (int): Director's id.
                data (DirectorIn): New attributes for the director.
            Returns:
                Any | None: Updated director. """

        if self._get_by_id(director_id):
            query = (
                director_table.update()
                .where(director_table.c.id == director_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            director = await self._get_by_id(director_id)
            return Director(**dict(director)) if director else None
        return None

    async def delete_director(self, director_id: int) -> bool:
        """The method for deleting a director from the database.
            Args:
                director_id (int): Director's id.
            Returns:
                bool: Operation's success."""
        if self._get_by_id(director_id):
            query = director_table \
                .delete() \
                .where(director_table.c.id == director_id)
            await database.execute(query)

            return True
        return False

    async def _get_by_id(self, director_id: int) -> Record | None:
        """A private method for getting a director from the db by its ID.
            Args:
                director_id (int): Director's id.
            Returns:
                Any | None: Director record if possible."""
        query = (director_table.select()
                 .where(director_table.c.id == director_id))
        return await database.fetch_one(query)