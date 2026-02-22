from typing import Optional

from libs.dataset_service.movie_dataset_service import MovieDatasetService
from libs.dtos.dataset_dto import MovieCharacterResponse, MovieSearchResponse


class DatasetUseCases:
    def __init__(self):
        self.movie_service = MovieDatasetService()

    def search_movie_characters(
        self,
        title_query: Optional[str] = None,
        genre: Optional[str] = None,
        min_imdb_rating: Optional[float] = None,
        release_year: Optional[str] = None,
        character_name: Optional[str] = None,
    ) -> MovieSearchResponse:
        results = self.movie_service.search_characters(
            title_query=title_query,
            genre=genre,
            min_imdb_rating=min_imdb_rating,
            release_year=release_year,
            character_name=character_name,
        )

        return MovieSearchResponse(
            results=[MovieCharacterResponse(**res) for res in results]
        )
