from typing import Optional

from fastapi import APIRouter, Query

from libs.dtos.dataset_dto import MovieSearchResponse
from libs.use_cases.dataset_use_cases import DatasetUseCases

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"],
    responses={404: {"description": "Not found"}},
)

dataset_use_cases = DatasetUseCases()


@router.get("/characters", response_model=MovieSearchResponse)
def search_characters(
    title: Optional[str] = Query(None, description="Wildcard search on movie title"),
    genre: Optional[str] = Query(None, description="Movie genre filter"),
    min_rating: Optional[float] = Query(None, description="Minimum IMDB rating filter"),
    year: Optional[str] = Query(None, description="Release year filter"),
    character_name: Optional[str] = Query(None, description="Wildcard search on character name"),
):
    """
    Search for movie characters by movie details.
    """
    return dataset_use_cases.search_movie_characters(
        title_query=title, genre=genre, min_imdb_rating=min_rating, release_year=year, character_name=character_name
    )
