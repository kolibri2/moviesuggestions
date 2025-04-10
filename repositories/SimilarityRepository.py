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

    def save_similar_movies(
        self, movie_id: int, similar_movies: List[Tuple[int, float]]
    ) -> None:
        pass

    def get_similar_movies(self, movie_id: int) -> List[Tuple[int, float]]:
        pass


class SQLSimilarityRepository(AbstractSimilarityRepository):

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_similarity_table()

    def _create_similarity_table(self):
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

    def add_similarity_score(self, movie_1_key, movie_2_key, similarity_score):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT INTO similarityScore (movie_1_ref, movie_2_ref, similarity_score) 
        VALUES (?,?,?); """,
            (movie_1_key, movie_2_key, similarity_score),
        )
        self.conn.commit()

    def get_similar_movies(self, movie_id: int) -> List[Tuple[int, float]]:
        pass
