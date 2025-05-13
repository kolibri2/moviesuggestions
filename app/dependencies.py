import sqlite3

from fastapi import Depends
from typing import Generator

from app.db import get_connection
from app.repositories.MovieRepository import SQLMovieRepository
from app.repositories.SimilarityRepository import SQLSimilarityRepository
from app.repositories.UserMoviePreferenceRepository import (
    SQLUserMoviePreferenceRepository,
)
from app.repositories.UserRepository import SQLUserRepository
from app.services.MovieService import MovieService
from app.services.RecommendationService import RecommendationService
from app.services.SimilarityService import SimilarityService
from app.services.UserMoviePreferenceService import UserMoviePreferenceService
from app.services.UserService import UserService

MOVIE_CSV_PATH = "../Data/archive/movies_metadata.csv"


def get_movie_service(
    conn=Depends(get_connection),
) -> Generator[MovieService, None, None]:
    repo = SQLMovieRepository(MOVIE_CSV_PATH, source=conn)
    svc = MovieService(repo)
    yield svc


def get_similarity_service(
    conn: sqlite3.Connection = Depends(get_connection),
    movie_service: MovieService = Depends(get_movie_service),
) -> Generator[SimilarityService, None, None]:
    sim_repo = SQLSimilarityRepository(conn)
    svc = SimilarityService(sim_repo, movie_service)
    yield svc


def get_user_service_old(
    conn=Depends(get_connection),
) -> Generator[UserService, None, None]:
    repo = SQLUserRepository(conn)  # repo takes a connection, not a path
    svc = UserService(repo)
    yield svc


def get_user_service(
    conn: sqlite3.Connection = Depends(get_connection),
) -> Generator[UserService, None, None]:
    repo = SQLUserRepository(conn)
    svc = UserService(repo)
    try:
        yield svc
    finally:
        # no need to close conn here; get_connection does that
        pass


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
