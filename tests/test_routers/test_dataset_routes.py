from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@patch("backend.routers.dataset_routes.dataset_use_cases.search_movie_characters")
def test_search_characters(mock_search):
    mock_search.return_value = MagicMock(
        results=[
            MagicMock(
                movie_id="m0",
                movie_title="10 things i hate about you",
                movie_year="1999",
                movie_imdb_rating="6.90",
                movie_genres=["comedy", "romance"],
                character_id="u0",
                character_name="BIANCA",
            )
        ]
    )

    # Needs to match the Pydantic dumping mechanism which expects dicts if we return MagicMock,
    # or just return a proper Mocking setup. Better yet, let's use the actual DTO.
    from libs.dtos.dataset_dto import MovieCharacterResponse, MovieSearchResponse

    mock_search.return_value = MovieSearchResponse(
        results=[
            MovieCharacterResponse(
                movie_id="m0",
                movie_title="10 things i hate about you",
                movie_year="1999",
                movie_imdb_rating="6.90",
                movie_genres=["comedy", "romance"],
                character_id="u0",
                character_name="BIANCA",
            )
        ]
    )

    response = client.get("/dataset/characters?title=things&genre=comedy")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["character_name"] == "BIANCA"

    mock_search.assert_called_once_with(
        title_query="things", genre="comedy", min_imdb_rating=None, release_year=None
    )
