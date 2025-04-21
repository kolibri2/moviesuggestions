# Movie Suggestions

This project generates personalized movie recommendations using Natural Language Processing (NLP). It combines movie
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

5. **Run the Project**  
  Interact with the API to run the project.
