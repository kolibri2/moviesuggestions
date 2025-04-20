from typing import List
import time

from app.domain.Movie import Movie

from app.repositories.MovieRepository import AbstractMovieRepository


class MovieService:
    """
    Movie service
    """

    def __init__(
            self,
            movie_repository: AbstractMovieRepository,

    ):
        self.movie_repository = movie_repository

    def get_all_movies(self) -> List[Movie]:
        """
        Implements the get_all_movies method from the AbstractMovieRepository class
        :return: List of Movie objects
        """
        return self.movie_repository.get_all_movies()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """
        Implements the get_movie_by_id method from the AbstractMovieRepository class
        :param movie_id:
        :return: Movie object
        """
        return self.movie_repository.get_movie_by_id(movie_id)

    def get_overview_by_id(self, movie_id) -> str:
        """
        Implements the get_overview_by_id method from the AbstractMovieRepository class
        :param movie_id:
        :return: str with description of the movie
        """
        return self.movie_repository.get_overview_by_id(movie_id)

    def get_multiple_movies_by_id(self, movie_internal_ids: List[int]) -> List[Movie]:
        """
        :param movie_internal_ids: list of integer IDs
        :return: List of Movie objects, in the same order
        """
        movies = [self.get_movie_by_id(movie_id) for movie_id in movie_internal_ids]
        return movies
