"""A module containing director endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from filmapi.container import Container
from filmapi.domain.director import Director, DirectorIn
from filmapi.services.idirector import IDirectorService

router = APIRouter()


@router.post("/create", response_model=Director, status_code = 201)
@inject
async def create_director(
        director: DirectorIn,
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> dict:
    """An endpoint for adding new directors.

    Args:
        director (DirectorIn): The director data.
        service (IDirectorService, optional): The injected service dependency.

    Returns:
        dict: The new director attributes."""

    new_director = await service.create_director(director)

    return new_director.model_dump() if new_director else {}


@router.get("/all", response_model=Iterable[Director], status_code=200)
@inject
async def get_all_directors(
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> Iterable:
    """An endpoint for getting all directors.

    Args:
        service (IDirectorService, optional): The injected service dependency.

    Returns:
        Iterable: The director attribute collection. """
    directors = await service.get_all_directors()
    return directors

@router.get ("/search", response_model=Iterable[Director], status_code=200)
@inject
async def get_director_by_name(
        name: str,
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> Iterable:
    """An endpoint for getting directors with the provided text in their name.

    Args:
        service (IDirectorService, optional): The injected service dependency
        name (string): Part of director's name.
    Returns:
        Iterable[Director]: The director attribute collection."""
    directors = await service.get_director_by_name(name)
    return directors


@router.get("/{director_id}", response_model=Director, status_code=200)
@inject
async def get_director_by_id(
        director_id: int,
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> dict:
    """An endpoint for getting all directors.

    Args:
        service (IDirectorService, optional): The injected service dependency.
        director_id (int): Director's id.

    Raises:
        HTTPException: 404 if director does not exist.

    Returns:
        Director: The director attribute. """
    if director := await service.get_director_by_id(director_id):
        return director.model_dump()
    raise HTTPException(status_code=404, detail="Director not found")

@router.put("/{director_id}", response_model=Director, status_code=201)
@inject
async def edit_director(
        director_id: int,
        updated_director: DirectorIn,
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> dict:
    """An endpoint for editing director data.

    Args:
        director_id (int): The id of the director.
        updated_director (DirectorIn): The edited director details.
        service (IDirectorService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if director does not exist.

    Returns:
        dict: The updated director details."""
    if await service.get_director_by_id(director_id=director_id):
        new_director = await service.edit_director(
            director_id=director_id,
            data=updated_director,
        )
        return new_director.model_dump() if new_director \
            else {}

    raise HTTPException(status_code=404, detail="Director not found.")

@router.delete("/{director_id}", status_code=204)
@inject
async def delete_director(
        director_id: int,
        service: IDirectorService = Depends(Provide[Container.director_service]),
) -> None:
    """An endpoint for deleting directors.

        Args:
            director_id (int): Director's id.
            service (IDirectorService, optional): The injected service dependency.

        Raises:
            HTTPException: 404 if director does not exist.

        Returns:
            dict: Empty if operation finished.
        """
    if await service.get_director_by_id(director_id=director_id):
        await service.delete_director(director_id)
        return

    raise HTTPException(status_code=404, detail="Director not found.")