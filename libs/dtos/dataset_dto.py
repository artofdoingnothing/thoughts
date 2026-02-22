from typing import List

from pydantic import BaseModel


class MovieCharacterResponse(BaseModel):
    movie_id: str
    movie_title: str
    movie_year: str
    movie_imdb_rating: str
    movie_genres: List[str]
    character_id: str
    character_name: str


class MovieSearchResponse(BaseModel):
    results: List[MovieCharacterResponse]
