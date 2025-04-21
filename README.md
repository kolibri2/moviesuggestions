# Movie Suggestions

This project generates personalized movie recommendations using NLP. It combines movie embeddings and user embeddings to calculate recommendation scores.

## How It Works

1. **Movie Embeddings:**
   For each movie, a movie description is used to generate a LLM embedding representation. These embeddings are meant to capture the semantic meaning of the movie description, and
   the goal is to be able to compare movies numerically with this embedding representation. A movie embedding belongs to \[
\mathbf{X} \in \mathbb{R}^{D \times 1} where $D$ is the dimension of the embedding vector.
\]
   

3. **User Embeddings:**  
   Each user is also represented as a numerical vector (embedding) that reflects their preferences based on past interactions. It has the same dimensions as a movie.

4. **Recommendation Score:**  
   By multiplying the movie embeddings with the user embeddings, the model calculates a score for each movie.  
   Higher scores indicate a stronger match between the user's preferences and the movie's features.

## Dataset

The dataset used for this project is the Kaggle Movies dataset. It provides the necessary information about movies for the recommendation model.

