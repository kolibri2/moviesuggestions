from abc import ABC, abstractmethod
import pandas as pd

from domain.Movie import Movie


class AbstractMovieRepository(ABC):
    @abstractmethod
    def get_all_movies(self):
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        pass


class InMemoryMovieRepository(AbstractMovieRepository):
    def __init__(self, movies_csv_path: str):
        self.movies = [
            Movie(movie_id, title, genres)
            for movie_id, title, genres in
            (zip(pd.read_csv(movies_csv_path)['movieId'].tolist(),
                 pd.read_csv(movies_csv_path)['title'].tolist(),
             pd.read_csv(movies_csv_path)['genres'].tolist())
             )
        ]
        self.ratings = []

    def get_all_movies(self) -> list[Movie]:
        return self.movies

    def get_movie(self, movie_id):
        pass


class SQLMovieRepository(AbstractMovieRepository):
    pass
