import torch
from transformers import DistilBertTokenizer, DistilBertModel
import torch.nn.functional as F
from typing import List
import time

from repositories.MovieRepository import AbstractMovieRepository


class MovieService:
    def __init__(self, movie_repository: AbstractMovieRepository):
        self.movie_repository = movie_repository
        self.tokenizer = None
        self.model = None


        #self.similarity_matrix = self.calculate_pairwise_similarity


    def get_all_movies(self):
        return self.movie_repository.get_all_movies()

    def get_movie_by_id(self, movie_id):
        return self.movie_repository.get_movie_by_id(movie_id)

    def get_overview_by_id(self, movie_id):
        return self.movie_repository.get_overview_by_id(movie_id)

    def initiate_llm(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
        self.model = DistilBertModel.from_pretrained('distilbert-base-cased')
        #return tokenizer, model

    def get_embeddings(self, texts):
        # Tokenize input texts and compute embeddings using the model
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Taking the mean of the token embeddings (this is one simple way to get a sentence embedding)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings


    def calculate_pairwise_similarity(self):
        # Ensure your model is initiated
        if self.tokenizer is None or self.model is None:
            self.initiate_llm()

        movie_internal_ids = [int(movie.internal_id) for movie in self.get_all_movies()]

        descriptions = [self.get_overview_by_id(movie_internal_id) for movie_internal_id in movie_internal_ids]

        embeddings = self.get_embeddings(descriptions[0:100])

        self.similarity_matrix = F.cosine_similarity(embeddings.unsqueeze(1), embeddings.unsqueeze(0), dim=-1)

        # Optionally, organize results in a dict (or any format you prefer)
        #similarity_scores = {}
        #num_movies = len(movies)
        # for i in range(num_movies):
        #for j in range(i+1, num_movies):
        # similarity_scores[(movies[i].movie_id, movies[j].movie_id)] = similarity_matrix[i][j]

        #return similarity_matrix

    def get_most_similar_by_id(self, movie_internal_id):
        """
        Returns a list of indices sorted by their corresponding values in descending order.

        Example:
          lst = [2, 7, 3, 10, 5]
          get_sorted_indices_desc(lst) -> [3, 1, 4, 2, 0]
        """
        movie_score_list = self.similarity_matrix[movie_internal_id]
        return sorted(range(len(movie_score_list)), key=lambda i: movie_score_list[i], reverse=True)

    def get_multiple_movies_by_id(self, movie_internal_ids: List[int]):
        movies = [self.get_movie_by_id(movie) for movie in movie_internal_ids]
        return movies[0:4]
