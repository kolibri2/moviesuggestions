import sqlite3
from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractSimilarityRepository(ABC):
    @abstractmethod
    def add_similarity_score(
        self, movie_1_ref, movie_2_ref, similarity_score: float
    ) -> None:
        pass

    @abstractmethod
    def get_similar_movies(self, movie_id: int) -> List[Tuple[int, float]]:
        pass


class SimilarityRepository(AbstractSimilarityRepository):

    def __init__(self):
        self.similar_movies = []

    def add_similarity_score(
        self, movie_1_key: int, movie_2_key: int, similarity_score: float
    ) -> None:
        pass

    def get_similar_movies(self, movie_id: int) -> List[Tuple[int, float]]:
        pass


class SQLSimilarityRepository(AbstractSimilarityRepository):
    """
    Implements the SimilarityRepository interface as a SQLite database.
    """

    def __init__(self, db_path: str):

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_similarity_table()

    def _create_similarity_table(self):
        """
        Creates the Similarity table.

        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
        
        CREATE TABLE if not exists similarityScore(
        
    similarity_score_key integer PRIMARY KEY AUTOINCREMENT,
    movie_1_ref integer,
    movie_2_ref integer,
    similarity_score float,
    FOREIGN KEY (movie_1_ref) REFERENCES movies (movie_key),
    FOREIGN KEY (movie_2_ref) REFERENCES movies (movie_key),
    UNIQUE (movie_1_ref, movie_2_ref)

)

"""
        )
        self.conn.commit()

    def add_similarity_score(
        self, movie_1_key: int, movie_2_key: int, similarity_score: float
    ):
        """
        Adds a similarity score to the Similarity table.
        :param movie_1_key:
        :param movie_2_key:
        :param similarity_score:

        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT INTO similarityScore (movie_1_ref, movie_2_ref, similarity_score) 
        VALUES (?,?,?)
        ON CONFLICT(movie_1_ref, movie_2_ref)
        DO UPDATE SET similarity_score = excluded.similarity_score; """,
            (movie_1_key, movie_2_key, similarity_score),
        )
        self.conn.commit()

    def get_similar_movies(self, movie_id: int) -> List[Tuple[int, float]]:
        """
        Gets a list of similar movies.
        :param movie_id:
        :return: List[Tuple[int, float]] of movie ids (int) and similarity scores (float).
        """
        cursor = self.conn.cursor()
        query = """
                SELECT s.movie_2_ref,
                m.movie_key,
                s.similarity_score
                FROM similarityScore s
                JOIN movies m
                ON s.movie_2_ref = m.movie_key
                WHERE s.movie_1_ref = ?
                ORDER BY s.similarity_score DESC
                LIMIT 5;
            """
        cursor.execute(query, (movie_id,))
        movie_list = cursor.fetchall()
        return movie_list
