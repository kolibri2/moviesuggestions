from typing import Optional

import numpy as np

from app.domain.User import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.UserRepository = user_repository

    def add_user(self, username: str, embedding_vector: Optional[np.ndarray] = None):
        user_added_bool = self.UserRepository.add_user(username, embedding_vector)
        return user_added_bool

    def get_user(self, user_id: int) -> User:
        if not self.UserRepository.get_user(user_id):
            return None
        return self.UserRepository.get_user(user_id)

    def get_user_id_by_username(self, username: str) -> Optional[int]:
        """
        Get user id from username
        :param username:
        :return:
        """

        return self.UserRepository.get_user_id_by_username(username)

    def update_embedding_vector(self, user_id: int, embedding_vector: np.ndarray):

        self.UserRepository.update_embedding_vector(user_id, embedding_vector)

    def get_embedding_vector(self, user_id: int) -> Optional[np.ndarray]:
        """
        Returns the user’s embedding array, or None if missing.
        """
        # 1) fetch once
        embedding = self.UserRepository.get_embedding_vector(user_id)

        # 2) if the repo gave us no row (None), signal no embedding
        if embedding is None:
            return None

        # 3) otherwise just pass it back
        return embedding
