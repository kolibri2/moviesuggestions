# Movie Suggestions

This project generates personalized movie recommendations using Natural Language Processing. It combines movie
embeddings and user embeddings to calculate recommendation scores.

## How It Works

1. **Movie Embeddings:**
   For each movie, a movie description is used to generate a LLM embedding representation. These embeddings are meant to
   capture the semantic meaning of the movie description, and
   the goal is to be able to compare movies numerically with this embedding representation.

2. **User Embeddings:**  
   Each user is also represented as a numerical vector (embedding) that reflects their preferences based on past
   interactions. It has the same dimensions as a movie.

3. **Recommendation Score:**  
   By multiplying the movie embeddings with the user embeddings, the model calculates a score for each movie.  
   Higher scores indicate a stronger match between the user's preferences and the movie's features.

## Dataset

The dataset used for this project
is [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset), which is available on Kaggle.  
You must download the dataset manually before running the project.

## Installation and Setup

Follow these steps to get started:

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/kolibri2/moviesuggestions.git
   cd moviesuggestions
   ```

2. **Install Dependencies**  
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Dataset**
    - Visit the [Kaggle Movies Dataset page](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).
    - Download the dataset and extract it locally.

4. **Set the Dataset Path**  
   Update the `MOVIE_CSV_PATH` variable in `main.py` to point to the location of the downloaded dataset file. For
   example:
   ```python
   MOVIE_CSV_PATH = "path/to/movies.csv"
   ```

## Interact with the API

The easiest way to interact with this project's API is through the `/docs` endpoint. It provides a built-in, interactive
API documentation interface.

### Accessing the API Documentation

1. Start the server by running the project:
   ```bash
   python main.py
   ```

Running `main.py` as is defaults to 100 movies being read from the dataset. This can be changed by altering
the `num_movies` parameter of `SQLMovieRepository` inititation in `init_new_db`, also in `main.py`.

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



