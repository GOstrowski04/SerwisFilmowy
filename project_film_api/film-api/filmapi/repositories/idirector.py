
from abc import ABC, abstractmethod
from typing import Any, Iterable

from filmapi.domain.director import Director, DirectorIn


class IDirectorRepository(ABC):
    @abstractmethod
    async def get_all_directors(self) -> Iterable[Any]:
        """Abstract for getting all directors.
        Returns:
            Iterable[Director]: Directors in database."""

    @abstractmethod
    async def get_director_by_name(self, name: str) -> Iterable[Any]:
        """Abstract for getting a director by a part of its name.
        Args:
            name (str): Part of the director's name.
        Returns:
            Iterable[Director]: Directors in database."""
    @abstractmethod
    async def get_director_by_id(self, director_id: int) -> Any | None:
        """Abstract for getting a director by its id.
        Args:
            director_id (int): Director's id
        Returns:
            Any | None: Director in database."""
    @abstractmethod
    async def create_director(self, data: DirectorIn) -> Any | None:
        """Abstract for creating a new director.
        Args:
            data (DirectorIn): Attributes of the director.
        Returns:
            Any | None: Created director. """

    @abstractmethod
    async def edit_director(self, director_id: int, data: DirectorIn) -> Any | None:
        """Abstract for editing a director's name.
        Args:
            director_id (int): The id of the director.
            data (DirectorIn): Attributes of the director.
        Returns:
            Any | None: The updated director."""

    @abstractmethod
    async def delete_director(self, director_id: int) -> bool:
        """Abstract for deleting a director.
        Args:
            director_id (int): The id of the director.
        Returns:
            bool: Success of the operation."""

