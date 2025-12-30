
from typing import Iterable

from filmapi.domain.director import Director, DirectorIn
from filmapi.repositories.idirector import IDirectorRepository
from filmapi.services.idirector import IDirectorService


class DirectorService(IDirectorService):
    """A class implementing the director service."""
    _repository: IDirectorRepository

    def __init__(self, repository: IDirectorRepository) -> None:
        """The initializer of the 'director service'.

        Args:
            repository (IDirectorRepository): The reference to the repository.
            """
        self._repository = repository

    async def get_all_directors(self) -> Iterable[Director]:
        """The abstract for getting all directors from the repository.
        Returns:
            Iterable[Director]: Directors in database."""
        return await self._repository.get_all_directors()

    async def get_director_by_name(self, name: str) -> Iterable[Director]:
        """The abstract for getting a director from the repository by a part of its name.
        Args:
            name (str): Part of the director's name.
        Returns:
            Iterable[Director]: Directors in database."""

        return await self._repository.get_director_by_name(name)

    async def get_director_by_id(self, director_id: int) -> Director | None:
        """The abstract for getting a director from the repository by its id.
        Args:
            director_id (int): Director's id
        Returns:
            Director | None: The director data if it exists."""
        return await self._repository.get_director_by_id(director_id)

    async def create_director(self, data: DirectorIn) -> Director | None:
        """The abstract for adding a new director to the repository.
        Args:
            data (DirectorIn): Attributes of the director.
        Returns:
            Director | None: The newly created director. """
        return await self._repository.create_director(data)

    async def edit_director(self, director_id: int, data: DirectorIn) -> Director | None:
        """The abstract for editing director data in the repository.
        Args:
            director_id (int): The id of the director.
            data (DirectorIn): Attributes of the director.
        Returns:
            Director | None: The updated director."""
        return await self._repository.edit_director(director_id, data)

    async def delete_director(self, director_id: int) -> bool:
        """Abstract for deleting a director.
        Args:
            director_id (int): The id of the director.
        Returns:
            bool: Success of the operation."""
        return await self._repository.delete_director(director_id)