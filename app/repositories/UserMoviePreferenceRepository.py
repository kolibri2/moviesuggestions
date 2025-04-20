import os
import sqlite3
from abc import ABC, abstractmethod
from typing import Union


class AbstractUserMoviePreferenceRepository(ABC):

    @abstractmethod
    def add_user_preference(self, user_preference):
        pass

    @abstractmethod
    def get_user_preference(self, user_preference):
        pass


class SQLUserMoviePreferenceRepository(AbstractUserMoviePreferenceRepository):
    # def __init__(self, db_path: str):
    # self.conn = sqlite3.connect(db_path)
    # self.create_user_movie_table()

    def __init__(self, source: Union[str, sqlite3.Connection]):
        if isinstance(source, sqlite3.Connection):
            self.conn = source  # injected connection
        else:
            # Fallback: open a new one (old behaviour)
            self.conn = sqlite3.connect(
                source,
                detect_types=sqlite3.PARSE_DECLTYPES,
                check_same_thread=False,  # so background tasks won’t crash
            )

        self.create_user_movie_table()

    def create_user_movie_table(self):

        cursor = self.conn.cursor()

        query = """
        CREATE TABLE if not exists user_movie_preferences (
      user_id    INTEGER NOT NULL,
      movie_key   INTEGER NOT NULL,
      liked      INTEGER NOT NULL CHECK(liked IN (0,1)),
      movie_title  TEXT NOT NULL,
      timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (user_id, movie_key),
      FOREIGN KEY (user_id)  REFERENCES users(user_id),
      FOREIGN KEY (movie_key) REFERENCES movies(movie_key),
      UNIQUE (user_id, movie_key)
    );
        """

        cursor.execute(query)
        self.conn.commit()

    def add_user_preference(self, user_id, movie_key, liked):

        cursor = self.conn.cursor()
        query = """
    INSERT INTO user_movie_preferences
      (user_id, movie_key, liked, movie_title)
    SELECT
      ?,        -- user_id
      ?,        -- movie_key
      ?,        -- liked
      title     -- movie_title from movies.title
    FROM movies
    WHERE movie_key = ?
    ON CONFLICT(user_id, movie_key) DO UPDATE
      SET liked       = excluded.liked,
          timestamp   = CURRENT_TIMESTAMP,
          movie_title = excluded.movie_title
          RETURNING movie_title;
    """
        params = (user_id, movie_key, int(liked), movie_key)
        cursor.execute(query, params)
        movie_title = cursor.fetchone()
        self.conn.commit()

        return movie_title

    def get_user_preference(self, user_id: int, movie_key: int) -> int:
        cursor = self.conn.cursor()
        query = """
        SELECT liked FROM user_movie_preferences WHERE user_id = ? AND movie_key = ?;
        """
        cursor.execute(query, (user_id, movie_key))
        return cursor.fetchone()[0]

    def get_seen_movies(self, user_id: int) -> list:
        cursor = self.conn.cursor()
        query = """
        SELECT movie_key, movie_title FROM user_movie_preferences WHERE user_id = ?;
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        if rows:
            return rows
        else:
            return None
