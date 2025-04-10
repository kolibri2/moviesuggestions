import sqlite3

import pandas as pd
from fastapi import Depends

from repositories.MovieRepository import SQLMovieRepository
from services.MovieService import MovieService


def load_csv(file_path: str) -> pd.DataFrame:
    try:
        csv_df = pd.read_csv(file_path)
        return csv_df
    except FileNotFoundError:
        raise Exception("CSV file not found.")
    except pd.errors.ParserError as e:
        raise Exception(e)


def init_db(MOVIE_CSV_PATH, DB_PATH):
    # Create a temporary instance that connects, creates the table, and loads movies.
    # You may want to add logic so that you do not re‑load if the table already exists.
    repo = SQLMovieRepository(MOVIE_CSV_PATH, num_movies=100, db_path=DB_PATH)
    # Close the connection after initialization.




def get_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


def get_movie_repo(db_path, num_movies=100, conn: sqlite3.Connection = Depends(get_connection)):
    repo = SQLMovieRepository(db_path, num_movies=num_movies, db_path=db_path)
    repo.conn = conn
    return repo


def get_movie_service(repo: SQLMovieRepository = Depends(get_movie_repo)):
    return MovieService(repo)
