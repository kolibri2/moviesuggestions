import json
from dataclasses import asdict
from typing import Union, List
import time

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

from domain.Movie import Movie
from repositories.MovieRepository import InMemoryMovieRepository, SQLMovieRepository
from repositories.SimilarityRepository import (
    SimilarityRepository,
    SQLSimilarityRepository,
)
from services.MovieService import MovieService
from services.SimilarityService import SimilarityService
from utils import init_db, get_movie_repo, get_movie_service

app = FastAPI()
MOVIE_CSV_PATH = "Data/archive/movies_metadata.csv"
DB_PATH = "Databases/movies.db"
# movie_service = MovieService(InMemoryMovieRepository(MOVIE_CSV_PATH))
# movie_repository = InMemoryMovieRepository(MOVIE_CSV_PATH)


# repo = InMemoryMovieRepository(MOVIE_CSV_PATH)
movie_repo = SQLMovieRepository(MOVIE_CSV_PATH, num_movies=1000, db_path=DB_PATH)
similarity_repo = SQLSimilarityRepository(DB_PATH)
mov_service = MovieService(movie_repo)
sim_service = SimilarityService(similarity_repo, mov_service)


# sim_service.calculate_pairwise_similarity(num_movies=1000)


# print(len(movie_service.get_all_movies()))
def get_movie_service() -> MovieService:
    return mov_service


def get_similarity_service() -> SimilarityService:
    return sim_service


@app.get("/all_movies")
def get_all_movies(
    movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_all_movies()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, f: Union[str, None] = None):
    return {"item_id": item_id, "q": q, "f": f}


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    movie = movie_service.get_movie_by_id(movie_id)
    return {"title": movie.title, "overview": movie.overview}


@app.get("/all_movies")
def get_all_movies(movie_service: MovieService = Depends(get_movie_service)):
    movies = movie_service.get_all_movies()
    # Convert your movies to a serializable format if necessary.
    return movies


@app.get("/similarity/{movie_internal_id}")
def get_similar_movies_by_id(
    movie_internal_id: int,
    movie_service: MovieService = Depends(get_movie_service),
    similarity_service: SimilarityService = Depends(get_similarity_service),
):
    similar_movie_ids = similarity_service.get_similar_movies_by_id(movie_internal_id)

    return movie_service.get_multiple_movies_by_id(similar_movie_ids)
