from typing import Optional

import numpy as np

from domain.User import User
from repositories import UserRepository


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
        return self.UserRepository.get_user_id_by_username(username)

    def update_embedding_vector(self, user_id: int, embedding_vector: np.ndarray):

        self.UserRepository.update_embedding_vector(user_id, embedding_vector)

    def get_embedding_vector(self, user_id: int) -> np.ndarray:
        if not self.UserRepository.get_embedding_vector(user_id):
            return None
        return self.UserRepository.get_embedding_vector(user_id)
