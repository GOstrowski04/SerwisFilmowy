"""Module providing containers injecting dependencies."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from filmapi.repositories.filmdb import FilmRepository
from filmapi.repositories.genredb import GenreRepository
from filmapi.repositories.directordb import DirectorRepository
from filmapi.repositories.user import UserRepository
from filmapi.repositories.watched_film import WatchedFilmRepository
from filmapi.services.film import FilmService
from filmapi.services.genre import GenreService
from filmapi.services.director import DirectorService
from filmapi.services.user import UserService
from filmapi.services.watched_film import WatchedFilmService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    film_repository = Singleton(FilmRepository)
    genre_repository = Singleton(GenreRepository)
    director_repository = Singleton(DirectorRepository)
    user_repository = Singleton(UserRepository)
    watched_film_repository = Singleton(WatchedFilmRepository)

    film_service = Factory(FilmService, repository=film_repository)
    genre_service = Factory(GenreService, repository=genre_repository)
    director_service = Factory(DirectorService, repository=director_repository)
    user_service = Factory(UserService, repository=user_repository)
    watched_film_service = Factory(WatchedFilmService, repository=watched_film_repository)
