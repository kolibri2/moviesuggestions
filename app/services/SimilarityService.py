from typing import List, Tuple, Union

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from app.repositories.MovieRepository import SQLMovieRepository
from app.services.MovieService import MovieService


class SimilarityService:
    """
    Computes sentence embeddings for movie overviews and persists them on the
    movie row, so recommendations are O(N) dot products instead of an O(N)
    transformer pass per request.
    """

    DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    DEFAULT_BATCH_SIZE = 32

    def __init__(
        self,
        movie_repository: SQLMovieRepository,
        movie_service: MovieService,
        model_name: str = DEFAULT_MODEL_NAME,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ):
        self.movie_repository = movie_repository
        self.movie_service = movie_service
        self.model_name = model_name
        self.batch_size = batch_size
        self.model = None

    def initiate_llm(self):
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Could not initiate model: {e}")

    def get_embeddings(self, texts: Union[str, List[str]]) -> torch.Tensor:
        if isinstance(texts, str):
            texts = [texts]

        if self.model is None:
            self.initiate_llm()

        return self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

    def populate_movie_embeddings(self) -> None:
        """
        Compute and persist an embedding for every movie that doesn't have one.
        Run this once at ingest. Recommendation queries then read from DB.
        """
        movies = self.movie_service.get_all_movies()
        if not movies:
            return

        existing_keys = {key for key, _ in self.movie_repository.get_all_embeddings()}
        pending = [m for m in movies if int(m.internal_id) not in existing_keys]
        if not pending:
            return

        overviews = [m.overview for m in pending]
        embeddings = self.get_embeddings(overviews).cpu().numpy()
        for movie, vector in zip(pending, embeddings):
            self.movie_repository.save_embedding(int(movie.internal_id), vector)

    def get_all_movie_embeddings(self) -> Tuple[torch.Tensor, List[int]]:
        rows = self.movie_repository.get_all_embeddings()
        if not rows:
            return torch.empty(0), []
        ids, vectors = zip(*rows)
        matrix = torch.from_numpy(np.stack(vectors).astype(np.float32))
        return matrix, list(ids)
