from dataclasses import dataclass


@dataclass
class Movie:
    movie_id: int
    title: str
    genres: str

