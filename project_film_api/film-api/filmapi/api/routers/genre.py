"""A module containing genre endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from filmapi.container import Container
from filmapi.domain.genre import Genre, GenreIn
from filmapi.services.igenre import IGenreService

router = APIRouter()


@router.post("/create", response_model=Genre, status_code = 201)
@inject
async def create_genre(
        genre: GenreIn,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict:
    """An endpoint for adding new genres.

    Args:
        genre (GenreIn): The genre data.
        service (IGenreService, optional): The injected service dependency.

    Returns:
        dict: The new genre attributes."""

    new_genre = await service.create_genre(genre)

    return new_genre.model_dump() if new_genre else {}


@router.get("/all", response_model=Iterable[Genre], status_code=200)
@inject
async def get_all_genres(
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> Iterable:
    """An endpoint for getting all genres.

    Args:
        service (IGenreService, optional): The injected service dependency.

    Returns:
        Iterable: The genre attribute collection. """
    genres = await service.get_all_genres()
    return genres

@router.get ("/search", response_model=Iterable[Genre], status_code=200)
@inject
async def get_genre_by_name(
        name: str,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> Iterable:
    """An endpoint for getting genres with the provided text in their name.

    Args:
        service (IGenreService, optional): The injected service dependency
        name (string): Part of genre's name.
    Returns:
        Iterable[Genre]: The genre attribute collection."""
    genres = await service.get_genre_by_name(name)
    return genres


@router.get("/{genre_id}", response_model=Genre, status_code=200)
@inject
async def get_by_id(
        genre_id: int,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict:
    """An endpoint for getting all genres.

    Args:
        service (IGenreService, optional): The injected service dependency.
        genre_id (int): Genre's id.

    Raises:
        HTTPException: 404 if genre does not exist.

    Returns:
        Genre: The genre attribute. """
    if genre := await service.get_by_id(genre_id):
        return genre.model_dump()
    raise HTTPException(status_code=404, detail="Genre not found")

@router.put("/{genre_id}", response_model=Genre, status_code=201)
@inject
async def edit_genre(
        genre_id: int,
        updated_genre: GenreIn,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> dict:
    """An endpoint for editing genre data.

    Args:
        genre_id (int): The id of the genre.
        updated_genre (GenreIn): The edited genre details.
        service (IGenreService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if genre does not exist.

    Returns:
        dict: The updated genre details."""
    if await service.get_by_id(genre_id=genre_id):
        new_genre = await service.edit_genre(
            genre_id=genre_id,
            data=updated_genre,
        )
        return new_genre.model_dump() if new_genre \
            else {}

    raise HTTPException(status_code=404, detail="Genre not found.")

@router.delete("/{genre_id}", status_code=204)
@inject
async def delete_genre(
        genre_id: int,
        service: IGenreService = Depends(Provide[Container.genre_service]),
) -> None:
    """An endpoint for deleting genres.

        Args:
            genre_id (int): Genre's id.
            service (IGenreService, optional): The injected service dependency.

        Raises:
            HTTPException: 404 if genre does not exist.

        Returns:
            dict: Empty if operation finished.
        """
    if await service.get_by_id(genre_id=genre_id):
        await service.delete_genre(genre_id)
        return

    raise HTTPException(status_code=404, detail="Genre not found.")