from unittest.mock import patch

from libs.dataset_service.movie_dataset_service import MovieDatasetService


def test_search_characters_filtering():
    service = MovieDatasetService()

    # Create mock dataset
    mock_data = [
        {
            "movieID": "m0",
            "movieTitle": "10 things i hate about you",
            "movieYear": "1999",
            "movieIMDBRating": "6.90",
            "movieGenres": ["comedy"],
            "characterID1": "u0",
            "characterName1": "BIANCA",
            "characterID2": "u1",
            "characterName2": "CAMERON",
        },
        {
            "movieID": "m1",
            "movieTitle": "the matrix",
            "movieYear": "1999",
            "movieIMDBRating": "8.70",
            "movieGenres": ["action", "sci-fi"],
            "characterID1": "u2",
            "characterName1": "NEO",
            "characterID2": "u3",
            "characterName2": "MORPHEUS",
        },
    ]

    with patch.object(service, "_get_stream", return_value=mock_data):
        # Apply filter
        results = service.search_characters(genre="sci-fi")
        assert len(results) == 2  # NEO and MORPHEUS
        assert results[0]["character_name"] == "NEO"
        assert results[1]["character_name"] == "MORPHEUS"

        # Test rating filter
        results = service.search_characters(min_imdb_rating=8.0)
        assert len(results) == 2

        # Test exact year
        results = service.search_characters(release_year="1999")
        assert len(results) == 4  # Both movies
