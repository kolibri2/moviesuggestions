import os
import sqlite3
from typing import Union, List

from fastapi import FastAPI, Depends

from app.dependencies import get_user_service, get_user_movie_service, get_recommendation_service, \
    get_movie_service, get_similarity_service
from app.repositories.MovieRepository import SQLMovieRepository
from app.repositories.SimilarityRepository import (
    SQLSimilarityRepository,
)
from app.services.MovieService import MovieService
from app.services.RecommendationService import RecommendationService
from app.services.SimilarityService import SimilarityService
from app.services.UserMoviePreferenceService import UserMoviePreferenceService
from app.services.UserService import UserService

app = FastAPI()
MOVIE_CSV_PATH = "../Data/archive/movies_metadata.csv"
DB_PATH = "../Databases/moviesuggestion.db"
SCHEMA_PATH = r"../Databases/schema.sql"


def init_new_db(conn: sqlite3.Connection):
    movie_repo = SQLMovieRepository(MOVIE_CSV_PATH, source=conn, is_new_db=True)
    movie_service = MovieService(movie_repo)
    similarity_repo = SQLSimilarityRepository(source=conn)
    sim_service = SimilarityService(similarity_repo, movie_service)


@app.on_event("startup")
async def on_startup():
    first_time = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    if first_time:
        print("Creating db and reading movies from csv...")
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        init_new_db(conn)

    print("App is running.")


@app.post("/users/")
def create_user(username: str, svc: UserService = Depends(get_user_service)):
    user_added_bool = svc.add_user(username)
    if user_added_bool:
        return f"User {username} added successfully."
    else:
        return f"Failed adding user {username}."


@app.post("/rate_movie")
def rate_movie(
        username: str,
        movie_id: int,
        movie_opinion: int,  # 0 for dislike, 1 for like
        user_svc: UserService = Depends(get_user_service),
        pref_svc: UserMoviePreferenceService = Depends(get_user_movie_service),
        rec_svc: RecommendationService = Depends(get_recommendation_service),
):
    user_id = user_svc.get_user_id_by_username(username)

    if user_id is None:
        return f"User {username} not found."

    else:
        movie_title = pref_svc.add_user_preference(user_id, movie_id, movie_opinion)

        rec_svc.update_user_embedding_vector(user_id, movie_id)
        if movie_opinion:
            return f"User {username} registered as liking the movie {movie_title[0]}."
        if movie_opinion == 0:
            return (
                f"User {username} registered as disliking the movie {movie_title[0]}."
            )


@app.get("/get_recommendation")
def get_recommendation(
        username: str,
        user_svc: UserService = Depends(get_user_service),
        rec_svc: RecommendationService = Depends(get_recommendation_service),
):
    user_id = user_svc.get_user_id_by_username(username)
    if user_id is None:
        return f"User {username} not found."
    return rec_svc.get_recommendation(user_id, 5)


@app.get("/user/seen_movies")
def get_seen_movies(
        username: str,
        user_svc: UserService = Depends(get_user_service),
        pref_svc: UserMoviePreferenceService = Depends(get_user_movie_service),
) -> List[str]:
    user_id = user_svc.get_user_id_by_username(username)
    movies = pref_svc.get_seen_movies(user_id)
    if movies:
        movie_keys, movie_titles = zip(*movies)
        return movie_titles
    else:
        return "No seen movies found."


@app.get("/all_movies")
def get_all_movies(
        movie_service: MovieService = Depends(get_movie_service),
):
    return movie_service.get_all_movies()


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    movie = movie_service.get_movie_by_id(movie_id)
    return {"title": movie.title, "overview": movie.overview}


@app.get("/all_movies")
def get_all_movies(movie_service: MovieService = Depends(get_movie_service)):
    movies = movie_service.get_all_movies()
    # Convert your movies to a serializable format if necessary.
    return movies
