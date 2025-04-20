from dataclasses import dataclass

import numpy as np


@dataclass
class User:
    username: str
    user_id: int
    embedding_vector: np.ndarray
