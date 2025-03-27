from typing import Union

from fastapi import FastAPI

from repositories.MovieRepository import InMemoryMovieRepository
from services.MovieService import MovieService

app = FastAPI()
MOVIE_CSV_PATH = "/Users/oscarwink/Desktop/MovieSwiper/Data/ml-latest-small/movies.csv"
movie_service = MovieService(InMemoryMovieRepository(MOVIE_CSV_PATH))


@app.get("/")
def get_all_movies():
    return movie_service.get_all_movies()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, f: Union[str, None] = None):
    return {"item_id": item_id, "q": q, "f": f}
