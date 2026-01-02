"""Module providing containers injecting dependencies."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from filmapi.repositories.filmdb import FilmRepository
from filmapi.repositories.genredb import GenreRepository
from filmapi.repositories.directordb import DirectorRepository
from filmapi.repositories.user import UserRepository
from filmapi.services.film import FilmService
from filmapi.services.genre import GenreService
from filmapi.services.director import DirectorService
from filmapi.services.user import UserService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    film_repository = Singleton(FilmRepository)
    genre_repository = Singleton(GenreRepository)
    director_repository = Singleton(DirectorRepository)
    user_repository = Singleton(UserRepository)

    film_service = Factory(FilmService, repository=film_repository)
    genre_service = Factory(GenreService, repository=genre_repository)
    director_service = Factory(DirectorService, repository=director_repository)
    user_service = Factory(UserService, repository=user_repository)
