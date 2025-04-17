from typing import List
import time

from domain.Movie import Movie
from repositories.MovieRepository import AbstractMovieRepository
from repositories.SimilarityRepository import AbstractSimilarityRepository


class MovieService:
    """
    Movie service
    """

    def __init__(
        self,
        movie_repository: AbstractMovieRepository,
        # similarity_repository: AbstractSimilarityRepository,
    ):
        self.movie_repository = movie_repository

    def get_all_movies(self) -> List[Movie]:
        """
        Implements the get_all_movies method from the AbstractMovieRepository class
        :return: List of Movie objects
        """
        return self.movie_repository.get_all_movies()

    def get_movie_by_id(self, movie_id) -> Movie:
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

    def get_multiple_movies_by_id(self, movie_internal_ids: List[int]):
        """
        Implements the get_multiple_movies_by_id method from the AbstractMovieRepository class
        :param movie_internal_ids:
        :return: List of ints, movie ids
        """
        movies = [
            self.get_movie_by_id(movie[0]) for movie in movie_internal_ids
        ]  # return 0 as that gives the movie ids, 1 gives sim score
        return movies[0:4]  # return the entries with top 5 sim score.
