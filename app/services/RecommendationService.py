import torch
from typing import Tuple, List

from app.domain.Movie import Movie
from app.services.MovieService import MovieService
from app.services.SimilarityService import SimilarityService
from app.services.UserMoviePreferenceService import UserMoviePreferenceService
from app.services.UserService import UserService


class RecommendationService:
    def __init__(
        self,
        user_service: UserService,
        user_movie_preference_service: UserMoviePreferenceService,
        similarity_service: SimilarityService,
        movie_service: MovieService,
    ):
        self.user_service = user_service
        self.user_movie_preference_service = user_movie_preference_service
        self.similarity_service = similarity_service
        self.movie_service = movie_service

        # weights
        self.beta = 1.0
        self.gamma = 0.5

    def get_recommendation(self, user_id: int, num_recs: int) -> List[Movie]:
        """
        Recommend the top `num_recs` unseen movies for `user_id`, based on
        embedding‐dot‐product similarity.
        """
        # 1) load all movie embeddings and their IDs as tensors
        movie_embeddings, movie_ids = self._load_movie_tensors()

        # 2) build the user’s embedding vector on the same device/dtype
        user_emb = self._prepare_user_embedding(user_id, movie_embeddings)

        # 3) compute similarity scores
        scores = movie_embeddings @ user_emb  # (N,)

        # 4) remove movies the user has already seen
        unseen_ids, unseen_scores = self._filter_seen(movie_ids, scores, user_id)

        # 5) pick top‑K unseen and fetch Movie objects
        return self._top_k_movies(unseen_ids, unseen_scores, num_recs)

    def _load_movie_tensors(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Returns:
            movie_embeddings: Tensor of shape (N, D)
            movie_ids:        Tensor of shape (N,) dtype long
        """
        embeddings, ids = self.similarity_service.get_all_movie_embeddings()
        device, dtype = embeddings.device, embeddings.dtype

        ids_tensor = (
            ids
            if isinstance(ids, torch.Tensor)
            else torch.tensor(ids, dtype=torch.long, device=device)
        )
        return embeddings, ids_tensor

    def _prepare_user_embedding(
        self, user_id: int, movie_embeddings: torch.Tensor
    ) -> torch.Tensor:
        """
        Fetches the user’s embedding (or zeros if none), and ensures it
        lives on the same device/dtype as `movie_embeddings`.
        """
        raw = self.user_service.get_embedding_vector(
            user_id
        )  # this is a np array, needs to be converted to Tensor
        device, dtype = movie_embeddings.device, movie_embeddings.dtype
        size = movie_embeddings.size(1)

        if raw is None:
            return torch.zeros(size, device=device, dtype=dtype)

        emb = raw if isinstance(raw, torch.Tensor) else torch.tensor(raw)

        if emb.dim() == 2 and emb.size(0) == 1:
            emb = emb.squeeze(0)
        return emb.to(device=device, dtype=dtype)

    def _filter_seen(
        self, movie_ids: torch.Tensor, scores: torch.Tensor, user_id: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Masks out any IDs the user has already seen, returning only
        unseen IDs and their corresponding scores.
        """
        seen = self.user_movie_preference_service.get_seen_movies(user_id)
        if not seen:
            # no seen movies → keep all
            mask = torch.ones_like(movie_ids, dtype=torch.bool)
        else:
            seen_ids, _ = zip(*seen)
            seen_tensor = torch.tensor(
                list(seen_ids), dtype=movie_ids.dtype, device=movie_ids.device
            )
            mask = ~torch.isin(movie_ids, seen_tensor)

        return movie_ids[mask], scores[mask]

    def _top_k_movies(
        self, candidate_ids: torch.Tensor, candidate_scores: torch.Tensor, k: int
    ) -> List[Movie]:
        """
        Picks the top‑k scoring IDs (or fewer if not enough candidates),
        converts to a list, and fetches Movie objects.
        """
        count = min(k, candidate_scores.size(0))
        if count == 0:
            return []

        _, idxs = torch.topk(candidate_scores, count)
        top_ids = candidate_ids[idxs].tolist()
        return self.movie_service.get_multiple_movies_by_id(top_ids)

    def update_user_embedding_vector(self, user_id: int, movie_id: int):

        new_user_embedding_vector = self._calculate_embedding_vector(
            user_id=user_id, movie_id=movie_id
        )

        self.user_service.update_embedding_vector(user_id, new_user_embedding_vector)

    def _calculate_embedding_vector(self, user_id: int, movie_id: int):
        # fetch the old user embedding vector
        old_user_embedding_vector = self.user_service.get_embedding_vector(user_id)

        # fetch the embedding of the movie description
        new_movie_embedding = self.get_embedding_of_movie(movie_id)

        device = new_movie_embedding.device
        dtype = new_movie_embedding.dtype
        # if no old embedding, start from zeros
        if old_user_embedding_vector is None:
            old_user_embedding_vector = torch.zeros_like(new_movie_embedding)
        else:
            # convert any list/np.ndarray → Tensor, or move an existing Tensor
            if isinstance(old_user_embedding_vector, torch.Tensor):
                old_user_embedding_vector = old_user_embedding_vector.to(
                    device=device, dtype=dtype
                )
            else:
                old_user_embedding_vector = torch.tensor(
                    old_user_embedding_vector, device=device, dtype=dtype
                )

        # fetch the movie preference of movie_id from usermovieprefsvc
        preference = self.user_movie_preference_service.get_user_preferences(
            user_id, movie_id
        )

        if preference == 1:
            new_user_embedding_vector = (
                old_user_embedding_vector + self.beta * new_movie_embedding
            )
        if preference == 0:
            new_user_embedding_vector = (
                old_user_embedding_vector - self.gamma * new_movie_embedding
            )

        # normalize
        norm = new_user_embedding_vector.norm(p=2)
        if norm > 0:
            new_user_embedding_vector = new_user_embedding_vector / norm
        return new_user_embedding_vector

    def get_user_id_by_username(self, username) -> int:
        return self.user_service.get_user_id_by_username(username)

    def get_embedding_of_movie(self, movie_id):
        """
        Returns the embedding of the given movie id
        :param movie_id: int
        :return:
        """
        overview = self.movie_service.get_overview_by_id(movie_id)
        return self.similarity_service.get_embeddings(overview)
