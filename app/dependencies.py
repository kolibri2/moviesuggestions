import sqlite3

from fastapi import Depends
from typing import Generator

from app.db import get_connection
from app.repositories.MovieRepository import SQLMovieRepository
from app.repositories.UserMoviePreferenceRepository import SQLUserMoviePreferenceRepository
from app.repositories.UserRepository import SQLUserRepository
from app.services.MovieService import MovieService
from app.services.RecommendationService import RecommendationService
from app.services.SimilarityService import SimilarityService
from app.services.UserMoviePreferenceService import UserMoviePreferenceService
from app.services.UserService import UserService

MOVIE_CSV_PATH = "../Data/archive/movies_metadata.csv"


def get_movie_repository(
        conn=Depends(get_connection),
) -> Generator[SQLMovieRepository, None, None]:
    yield SQLMovieRepository(MOVIE_CSV_PATH, source=conn)


def get_movie_service(
        repo: SQLMovieRepository = Depends(get_movie_repository),
) -> Generator[MovieService, None, None]:
    yield MovieService(repo)


def get_similarity_service(
        movie_repo: SQLMovieRepository = Depends(get_movie_repository),
        movie_service: MovieService = Depends(get_movie_service),
) -> Generator[SimilarityService, None, None]:
    yield SimilarityService(movie_repo, movie_service)


def get_user_service(
        conn=Depends(get_connection),
) -> Generator[UserService, None, None]:
    repo = SQLUserRepository(conn)  # repo takes a connection, not a path
    svc = UserService(repo)
    yield svc


def get_user_movie_service(
        conn=Depends(get_connection),
) -> Generator[UserMoviePreferenceService, None, None]:
    repo = SQLUserMoviePreferenceRepository(conn)
    svc = UserMoviePreferenceService(repo)
    yield svc


def get_recommendation_service(
        movie_service: MovieService = Depends(get_movie_service),
        simil_service: SimilarityService = Depends(get_similarity_service),
        user_service: UserService = Depends(get_user_service),
        pref_service: UserMoviePreferenceService = Depends(get_user_movie_service),
) -> Generator[RecommendationService, None, None]:
    svc = RecommendationService(
        user_service,
        pref_service,
        simil_service,
        movie_service,
    )
    yield svc
