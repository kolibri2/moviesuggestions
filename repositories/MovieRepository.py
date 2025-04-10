import os
import sqlite3
import time
from abc import ABC, abstractmethod
import pandas as pd

from domain.Movie import Movie


class AbstractMovieRepository(ABC):
    @abstractmethod
    def get_all_movies(self):
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        pass


class InMemoryMovieRepository(AbstractMovieRepository):
    def __init__(self, movies_csv_path: str):
        movies_df = pd.read_csv(movies_csv_path, dtype={10: str})

        # self.movies = []
        # self.movies = [
        #     Movie(movie_id, title, overview)
        #     for movie_id, title, overview in
        #     (zip(movies_df['id'].tolist(),
        #          movies_df['title'].tolist(),
        #          movies_df['overview'].tolist())
        #      )
        # ]
        self.movies = []
        internal_id = 0
        for movie_id, title, overview in zip(
                movies_df['id'].tolist(),
                movies_df['title'].tolist(),
                movies_df['overview'].tolist()
        ):
            try:
                if type(overview) is str:
                    self.movies.append(Movie(movie_id, title, overview, internal_id))
                    internal_id += 1
                else:
                    continue
            except Exception as e:
                print(f"Skipping movie with non-int id: {movie_id}")
        print(f"InMemoryMovieRepository initialized {len(self.movies)} movies")

        self.ratings = []

    def get_all_movies(self) -> list[Movie]:
        return self.movies

    def get_movie_by_id(self, movie_id: int) -> Movie:
        return self.movies[movie_id]

    def get_overview_by_id(self, movie_id: int) -> str:
        return self.movies[movie_id].overview


class SQLMovieRepository(AbstractMovieRepository):

    def __init__(self, movies_csv_path: str, num_movies: int, db_path: str = ":memory", ):
        """

        :type num_movies: object
        """
        self.conn = sqlite3.connect(db_path)
        self._create_movies_table()

        is_new_db = os.path.exists(db_path)
        if is_new_db:
            self._load_movies_from_csv(movies_csv_path, num_movies)
        else:
            print("db already exists")

    def _create_movies_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
        internal_id integer PRIMARY KEY AUTOINCREMENT,
        movie_id TEXT UNIQUE,
        title TEXT,
        overview TEXT
        );
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _load_movies_from_csv(self, movies_csv_path: str, num_movies: int):

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM movies;")
        self.conn.commit()
        movies_df = pd.read_csv(movies_csv_path, dtype={10: str})

        movies_added = 0
        for movie_id, title, overview in zip(
                movies_df['id'].tolist(),
                movies_df['title'].tolist(),
                movies_df['overview'].tolist()
        ):
            if isinstance(overview, str):
                self._insert_movie(movie_id, title, overview, )
                movies_added += 1
                if movies_added == num_movies:
                    break

            else:
                #print(f"Skipping movie with id: {movie_id}")
                continue
        print(f"SQLMovieRepository initialized {movies_added} movies")

    def _insert_movie(self, movie_id: int, title, overview):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO movies (movie_id, title, overview) VALUES (?, ?, ?)",
            (movie_id, title, overview)
        )
        self.conn.commit()

    def get_all_movies(self) -> list[Movie]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT internal_id, movie_id, title, overview FROM movies")
        rows = cursor.fetchall()
        movies = [Movie(movie_id, title, overview, internal_id) for internal_id, movie_id, title, overview in rows]
        return movies

    def get_movie_by_id(self, internal_id: int) -> Movie:
        cursor = self.conn.cursor()
        cursor.execute("SELECT internal_id, movie_id, title, overview FROM movies WHERE internal_id = ?",
                       (internal_id,))
        row = cursor.fetchone()
        if row:
            fetched_internal_id, movie_id, title, overview = row
            return Movie(movie_id, title, overview, internal_id)
        raise ValueError(f"Movie with internal id {internal_id} not found")

    def get_overview_by_id(self, internal_id: int) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT overview FROM movies WHERE internal_id = ?", (internal_id,))
        row = cursor.fetchone()
        if row:
            return row[0]
        raise ValueError(f"Overview from movie with internal id {internal_id} not found")
