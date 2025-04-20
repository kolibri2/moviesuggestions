import json
import sqlite3
from abc import ABC, abstractmethod
from typing import Union

import numpy as np

from app.domain.User import User


class AbstractUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def add_user(self, username):
        pass

    @abstractmethod
    def update_embedding_vector(self, user_id, embedding_vector):
        pass


class SQLUserRepository(AbstractUserRepository):

    # def __init__(self, db_path: str):
    # self.conn = sqlite3.connect(db_path)
    # self._create_user_table()

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
        self._create_user_table()

    def _create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        embedding_vector float,
        UNIQUE(username)
        );"""
        )
        self.conn.commit()

    def get_user(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE user_id=?""",
            user_id,
        )
        row = cursor.fetchone()
        if row is None:

            return None
        else:
            return User(row[0], row[1], row[2])

    def get_user_id_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username=?;", (username,))
        row = cursor.fetchone()
        if row is None:
            print(f"User {username} does not exist")
            return None
        else:
            return row[0]

    def add_user(self, username: str, embedding_vector: np.ndarray = None):

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, embedding_vector) VALUES (?, ?)",
                (username, embedding_vector),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # this fires if username already exists
            self.conn.rollback()
            print(f"User “{username}” already exists!")
            return False

    def update_embedding_vector(self, user_id: int, embedding_vector):
        # the embedding vector is converted to a json in order to be able to save it using SQLite
        if hasattr(embedding_vector, "detach"):
            embedding_vector = embedding_vector.detach().cpu().numpy().tolist()
        serialized = json.dumps(embedding_vector)

        cursor = self.conn.cursor()
        query = "UPDATE users SET embedding_vector=? WHERE user_id=?"
        cursor.execute(query, (serialized, user_id))
        self.conn.commit()

    def get_embedding_vector(self, user_id: int) -> np.ndarray:
        cursor = self.conn.cursor()
        query = "SELECT embedding_vector FROM users WHERE user_id=?;"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        # 1) no such user → no embedding
        if row is None:
            return None
        raw_json = row[0]
        if raw_json is None:
            return None

        print("returned embedding")
        vec_list = json.loads(raw_json)
        return np.array(vec_list, dtype=float)  # the embedding is a np.array
