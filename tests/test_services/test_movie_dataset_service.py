import os
import tempfile
from libs.dataset_service.movie_dataset_service import MovieDatasetService

def test_search_characters_filtering():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock dataset files
        titles_content = (
            "m0 +++$+++ 10 things i hate about you +++$+++ 1999 +++$+++ 6.90 +++$+++ 100 +++$+++ ['comedy']\n"
            "m1 +++$+++ the matrix +++$+++ 1999 +++$+++ 8.70 +++$+++ 100 +++$+++ ['action', 'sci-fi']\n"
        )
        chars_content = (
            "u0 +++$+++ BIANCA +++$+++ m0 +++$+++ 10 things i hate about you +++$+++ f +++$+++ 1\n"
            "u1 +++$+++ CAMERON +++$+++ m0 +++$+++ 10 things i hate about you +++$+++ m +++$+++ 2\n"
            "u2 +++$+++ NEO +++$+++ m1 +++$+++ the matrix +++$+++ m +++$+++ 1\n"
            "u3 +++$+++ MORPHEUS +++$+++ m1 +++$+++ the matrix +++$+++ m +++$+++ 2\n"
        )
        
        with open(os.path.join(temp_dir, "movie_titles_metadata.txt"), "w") as f:
            f.write(titles_content)
            
        with open(os.path.join(temp_dir, "movie_characters_metadata.txt"), "w") as f:
            f.write(chars_content)
            
        service = MovieDatasetService(data_dir=temp_dir)

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

        # Test partial character name match
        results = service.search_characters(character_name="BIAN")
        assert len(results) == 1
        assert results[0]["character_name"] == "BIANCA"

        # Test partial character name case-insensitive
        results = service.search_characters(character_name="neo")
        assert len(results) == 1
        assert results[0]["character_name"] == "NEO"
