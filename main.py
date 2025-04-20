from typing import Union, List, Generator

from fastapi import FastAPI, Depends

from domain.Movie import Movie
from repositories.MovieRepository import InMemoryMovieRepository, SQLMovieRepository
from repositories.SimilarityRepository import (
    SimilarityRepository,
    SQLSimilarityRepository,
)
from repositories.UserMoviePreferenceRepository import SQLUserMoviePreferenceRepository
from repositories.UserRepository import SQLUserRepository
from services.MovieService import MovieService
from services.RecommendationService import RecommendationService
from services.SimilarityService import SimilarityService
from services.UserMoviePreferenceService import UserMoviePreferenceService
from services.UserService import UserService
from db import get_connection

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

user_repo = SQLUserRepository(DB_PATH)
user_service = UserService(user_repo)

usr_movie_repo = SQLUserMoviePreferenceRepository(DB_PATH)
pref_svc = UserMoviePreferenceService(usr_movie_repo)

rec_svc = RecommendationService(user_service, pref_svc, sim_service, mov_service)


# sim_service.calculate_pairwise_similarity(num_movies=1000)


# print(len(movie_service.get_all_movies()))
# def get_movie_service(
#     conn=Depends(get_connection),
# ) -> Generator[MovieService, None, None]:
#     repo = SQLMovieRepository(conn)
#     svc = SimilarityService(repo, mov_service)
#     yield svc
#
#
# def get_similarity_service(
#     conn=Depends(get_connection),
# ) -> Generator[SimilarityService, None, None]:
#     repo = SQLSimilarityRepository(conn)
#     svc = SimilarityService(repo)
#     yield svc


def get_movie_service() -> MovieService:
    return mov_service


def get_similarity_service() -> SimilarityService:
    return sim_service


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
    conn=Depends(get_connection()),
) -> Generator[RecommendationService, None, None]:
    pref_repo = SQLUserMoviePreferenceRepository(conn)
    pref_svc = UserMoviePreferenceService(pref_repo)

    user_repo = SQLUserRepository(conn)
    user_svc = UserService(user_repo)

    movie_repo = SQLMovieRepository(conn)
    movie_svc = MovieService(movie_repo)

    sim_repo = SQLSimilarityRepository(conn)
    sim_svc = SimilarityService(user_svc, sim_repo)
    return rec_svc


@app.post("/users/")
def create_user(username: str, svc: UserService = Depends(get_user_service)):
    user_added_bool = svc.add_user(username)
    if user_added_bool:
        return f"User {username} added successfully"
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
