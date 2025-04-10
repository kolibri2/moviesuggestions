import json
from dataclasses import asdict
from typing import Union, List
import time

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

from domain.Movie import Movie
from repositories.MovieRepository import InMemoryMovieRepository, SQLMovieRepository
from services.MovieService import MovieService
from utils import init_db, get_movie_repo, get_movie_service

app = FastAPI()
MOVIE_CSV_PATH = "Data/archive/movies_metadata.csv"
DB_PATH = "Databases/movies.db"
#movie_service = MovieService(InMemoryMovieRepository(MOVIE_CSV_PATH))
#movie_repository = InMemoryMovieRepository(MOVIE_CSV_PATH)


repo = InMemoryMovieRepository(MOVIE_CSV_PATH)
#repo = SQLMovieRepository(MOVIE_CSV_PATH, num_movies=100, db_path=DB_PATH)
movie_service = MovieService(repo)
print(movie_service.get_all_movies()[0])
movie_service.calculate_pairwise_similarity()


#@app.on_event("startup")
def startup_event():
    init_db(MOVIE_CSV_PATH, DB_PATH)




@app.get("/all_movies")
def get_all_movies():
    return movie_service.get_all_movies()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, f: Union[str, None] = None):
    return {"item_id": item_id, "q": q, "f": f}


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    return movie_service.get_movie_by_id(movie_id).title, movie_service.get_movie_by_id(movie_id).overview


@app.get("/simil/{movie_internal_id}", response_class=HTMLResponse)
def get_similar_movies_by_id(movie_internal_id: int):
    similar_ids = movie_service.get_most_similar_by_id(movie_internal_id)
    movies = movie_service.get_multiple_movies_by_id(similar_ids)

    # Convert dataclass instances to dictionaries.
    movies_dict = [asdict(movie) for movie in movies]

    # Separate the first element as the "input movie" and the rest as "similar movies"
    if movies_dict:
        output = {
            "input_movie": movies_dict[0],
            "similar_movies": movies_dict[1:],
        }
    else:
        output = {"input_movie": None, "similar_movies": []}

    pretty_json = json.dumps(output, indent=4, sort_keys=True)

    # Wrap the JSON string in <pre> tags so the formatting shows in the browser
    html_content = f"<pre>{pretty_json}</pre>"
    return HTMLResponse(content=html_content)


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, service: MovieService = Depends(get_movie_service)):
    movie = service.get_movie_by_id(movie_id)
    return {"title": movie.title, "overview": movie.overview}


@app.get("/all_movies")
def get_all_movies(service: MovieService = Depends(get_movie_service)):
    movies = service.get_all_movies()
    # Convert your movies to a serializable format if necessary.
    return movies


@app.get("/simil/{movie_internal_id}")
def get_similar_movies_by_id(movie_internal_id: int, service: MovieService = Depends(get_movie_service)):
    # Adjust your call according to the implementation of your service.
    overview = service.get_overview_by_id(movie_internal_id)
    return {"overview": overview}
