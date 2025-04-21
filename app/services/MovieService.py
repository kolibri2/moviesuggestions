from typing import List
import time

from app.domain.Movie import Movie

from app.repositories.MovieRepository import AbstractMovieRepository


class MovieService:

    def __init__(
        self,
        movie_repository: AbstractMovieRepository,
    ):
        self.movie_repository = movie_repository

    def get_all_movies(self) -> List[Movie]:

        return self.movie_repository.get_all_movies()

    def get_movie_by_id(self, movie_id: int) -> Movie:

        return self.movie_repository.get_movie_by_id(movie_id)

    def get_overview_by_id(self, movie_id) -> str:

        return self.movie_repository.get_overview_by_id(movie_id)

    def get_multiple_movies_by_id(self, movie_internal_ids: List[int]) -> List[Movie]:

        movies = [self.get_movie_by_id(movie_id) for movie_id in movie_internal_ids]
        return movies
