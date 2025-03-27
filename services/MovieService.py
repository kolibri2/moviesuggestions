from repositories.MovieRepository import AbstractMovieRepository


class MovieService:
    def __init__(self, movie_repository: AbstractMovieRepository):
        self.movie_repository = movie_repository

    def get_all_movies(self):
        return self.movie_repository.get_all_movies()
