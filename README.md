# Movie suggestions

This project generates personalized movie recommendations using NLP. It uses an LLM (`distilbert/distilbert-base-cased`) to generate embeddings of movie descriptions. These embeddings are then used to calculate a similarity score, which in turn are used to recommend movies to users based on how they've rated movies.

## How it works

1. **Movie embeddings:**
   For each movie, a movie description is used to generate a LLM embedding representation. These embeddings are meant to
   capture the semantic meaning of the movie description, and
   the goal is to be able to compare movies numerically with this embedding representation.

2. **User embeddings:**  
   Each user is also represented as a numerical vector (embedding) that reflects their preferences based on how they
   have rated movies. It has the same dimensions as a movie embedding.

3. **Recommendation score:**  
   By multiplying the movie embeddings with the user embeddings, the model calculates a score for each movie.  
   Higher scores indicate a stronger match between the user's preferences and the movie's features.

## Dataset

The dataset used for this project
is [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset), which is available on Kaggle.  
Download the dataset manually before running the project.

## Installation and setup

Follow these steps to get started:

1. **Clone the repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/kolibri2/moviesuggestions.git
   cd moviesuggestions
   ```

2. **Install dependencies**  
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Interact with the API

The easiest way to interact with this project's API is through the `/docs` endpoint.

### Run the project

> ❗ **Dataset download**
> The first run will automatically download a ~12 MB CSV dataset from Kaggle.

1. Start the server by running the project from project root:
   ```bash
   make run
   ```

Running as is defaults to 100 movies being read from the dataset. This can be changed by altering
the `num_movies` parameter of `init_new_db`, inside the API startup function `on_startup` in `main.py`.

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```

3. Explore the API:
    - You can test all available endpoints, such as creating users, rating movies, and getting movie recommendations.
    - The interface allows you to input parameters and see live responses from the API.

### API Use Cases

A user can be created with:

```bash
   curl -X 'POST' 'http://127.0.0.1:8000/users?username={USERNAME}' 
   ```

With a user created, a movie can be rated by that user. A ```
movie_id``` needs to be provided, alongside a ```rating``` of the movie where ```1``` is like and ```0``` is dislike:

   ```bash
   curl -X 'POST' 'http://127.0.0.1:8000/rate_movie?username={USERNAME}&movie_id={MOVIE_ID}&rating={RATING}' 
   ```

A user can get personalized movie recommendations with:

   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/get_recommendation?username={USERNAME}'
   ```



