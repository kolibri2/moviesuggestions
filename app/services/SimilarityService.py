import numpy as np
import torch
from sklearn.decomposition import PCA
from transformers import DistilBertTokenizer, DistilBertModel
import torch.nn.functional as F
from app.repositories import SimilarityRepository, MovieRepository
from typing import List, Tuple, Union

from app.services.MovieService import MovieService


class SimilarityService:
    """
    Service for computing and storing pairwise text similarity scores
    between movie overviews using a DistilBERT-based embedding model.
    """

    DEFAULT_MODEL_NAME = "distilbert-base-cased"
    DEFAULT_BATCH_SIZE = 32

    def __init__(
        self,
        similarity_repository: SimilarityRepository,
        movie_service: MovieService,
        model_name: str = DEFAULT_MODEL_NAME,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ):
        """
        Args:
            similarity_repository: Repository for saving and retrieving similarity scores.
            model_name: Name of the pretrained DistilBERT model to load.
            batch_size: Number of texts to process per batch when computing embeddings.
        """
        self.similarity_matrix = None
        self.similarity_repository = similarity_repository
        self.movie_service = movie_service
        self.tokenizer = None
        self.model = None
        self.model_name = model_name
        self.batch_size = batch_size

    def initiate_llm(self):
        """
        Initialize the similarity scores using an embedding model.
        """
        try:
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            self.model = DistilBertModel.from_pretrained(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Could not initiate model: {e}")

    def get_all_movie_embeddings(self):

        movie_internal_ids = [
            int(movie.internal_id) for movie in self.movie_service.get_all_movies()
        ]
        descriptions = [
            self.movie_service.get_overview_by_id(movie_internal_id)
            for movie_internal_id in movie_internal_ids
        ]

        # 3. Calculate the model embeddings.
        embeddings = self.get_embeddings(descriptions)
        return embeddings, movie_internal_ids

    def get_embeddings(self, texts: Union[str, List[str]]) -> torch.Tensor:
        """
        Compute embeddings for a list of texts.
        :param texts: List of texts to compute embeddings for.
        :return: Embeddings for a list of texts.
        """

        # Normalize input to list
        single = False
        if isinstance(texts, str):
            texts = [texts]
            single = True

        if self.tokenizer is None or self.model is None:
            self.initiate_llm()

        # Tokenize input texts and compute embeddings using the model
        inputs = self.tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        # taking the mean of the token embeddings
        embeddings = outputs.last_hidden_state.mean(dim=1)
        print(embeddings.shape)
        embeddings_debiased = self._remove_principal_component(
            embeddings
        )  # remove the component that is common along all embeddings in order to get a better similarity score.

        return embeddings_debiased

    def _remove_principal_component(self, embeddings: torch.Tensor) -> torch.Tensor:
        """
        Debias embeddings by removing their first principal component via PCA.
        """
        # Move embeddings to CPU and convert to numpy for PCA
        embeddings_np = embeddings.cpu().detach().numpy()
        pca = PCA(n_components=1)
        pca.fit(embeddings_np)
        principal_axis = pca.components_[0]  # shape (D,)

        # Convert principal axis back to torch tensor
        principal_vector = (
            torch.from_numpy(principal_axis).to(embeddings.device).to(embeddings.dtype)
        )  # shape (D,)

        # Compute projection of each embedding onto the principal vector
        projection_scores = embeddings.matmul(principal_vector)  # shape (N,)

        # Subtract the projected component
        debiased = embeddings - projection_scores.unsqueeze(
            1
        ) * principal_vector.unsqueeze(0)

        # L2 normalize debiased embeddings
        normalized = F.normalize(debiased, p=2, dim=1)
        return normalized

    def calculate_pairwise_similarity(
        self,
        num_movies: int = 100,
    ):
        """
        Calculate the pairwise similarity scores, using the get_embeddings method and all the movies read into the
        movie repository.
        """
        # 1. Ensure your model is initiated

        # 2. fetch the movie ids in the repo, then fetch all the corresponding descriptions.
        movie_internal_ids = [
            int(movie.internal_id) for movie in self.movie_service.get_all_movies()
        ]
        descriptions = [
            self.movie_service.get_overview_by_id(movie_internal_id)
            for movie_internal_id in movie_internal_ids
        ]

        # 3. Calculate the model embeddings.
        embeddings = self.get_embeddings(descriptions[0:num_movies])

        # 4. Calculate the pairwise similarity score between all embeddings.
        self.similarity_matrix = F.cosine_similarity(
            embeddings.unsqueeze(1), embeddings.unsqueeze(0), dim=-1
        )

        # 5. Loop through the similarity matrix and write the pairwise similarity score to database.
        similarity_matrix_size = self.similarity_matrix.size(0)
        for movie_1_key in range(similarity_matrix_size):
            for movie_2_key in range(similarity_matrix_size):
                value = self.similarity_matrix[movie_1_key, movie_2_key].item()
                self.similarity_repository.add_similarity_score(
                    movie_1_key, movie_2_key, value
                )

    def get_similar_movies_by_id(
        self, movie_internal_id: int
    ) -> List[Tuple[int, float]]:
        """
        Get a list of movie ids similar to the given movie internal ID.
        :param movie_internal_id:
        :return: List of Tuples of movie id and similarity score.
        """
        return self.similarity_repository.get_similar_movies(movie_internal_id)
