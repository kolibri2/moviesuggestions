from dataclasses import dataclass


@dataclass
class Movie:
    movie_id: int
    title: str
    overview: str #plot description
    internal_id: int

