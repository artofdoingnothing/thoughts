from typing import List, Optional

from datasets import load_dataset


class MovieDatasetService:
    def __init__(self):
        # We don't load everything into memory. We initialize a streaming dataset.
        pass

    def _get_stream(self):
        return load_dataset(
            "cornell_movie_dialog",
            split="train",
            streaming=True,
            trust_remote_code=True,
        )

    def search_characters(
        self,
        title_query: Optional[str] = None,
        genre: Optional[str] = None,
        min_imdb_rating: Optional[float] = None,
        release_year: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        stream = self._get_stream()
        results = []

        # We need to deduplicate characters since multiple dialogues can have the same character
        seen_characters = set()

        for row in stream:
            if len(results) >= limit:
                break

            movie_title = row.get("movieTitle", "").strip()
            movie_year = row.get("movieYear", "").strip()
            movie_rating_str = row.get("movieIMDBRating", "").strip()
            movie_genres = row.get("movieGenres", [])

            # Filtering
            if title_query and title_query.lower() not in movie_title.lower():
                continue

            if genre and genre.lower() not in [g.lower() for g in movie_genres]:
                continue

            if release_year and release_year != movie_year:
                continue

            if min_imdb_rating is not None:
                try:
                    rating = float(movie_rating_str)
                    if rating < min_imdb_rating:
                        continue
                except ValueError:
                    continue  # Skip if no valid rating

            # Valid movie match, now extract characters.
            # cornell movie dialog rows represent interactions between two characters
            char1_id = row.get("characterID1", "").strip()
            char1_name = row.get("characterName1", "").strip()
            char2_id = row.get("characterID2", "").strip()
            char2_name = row.get("characterName2", "").strip()

            char1_key = f"{row.get('movieID')}_{char1_id}"
            if char1_id and char1_name and char1_key not in seen_characters:
                seen_characters.add(char1_key)
                results.append(
                    {
                        "movie_id": row.get("movieID", "").strip(),
                        "movie_title": movie_title,
                        "movie_year": movie_year,
                        "movie_imdb_rating": movie_rating_str,
                        "movie_genres": movie_genres,
                        "character_id": char1_id,
                        "character_name": char1_name,
                    }
                )

            if len(results) >= limit:
                break

            char2_key = f"{row.get('movieID')}_{char2_id}"
            if char2_id and char2_name and char2_key not in seen_characters:
                seen_characters.add(char2_key)
                results.append(
                    {
                        "movie_id": row.get("movieID", "").strip(),
                        "movie_title": movie_title,
                        "movie_year": movie_year,
                        "movie_imdb_rating": movie_rating_str,
                        "movie_genres": movie_genres,
                        "character_id": char2_id,
                        "character_name": char2_name,
                    }
                )

        return results

    def get_character_dialogues(self, character_id: str, limit: int = 100) -> List[List[str]]:
        stream = self._get_stream()
        dialogues = []

        for row in stream:
            if len(dialogues) >= limit:
                break
            
            char1_id = row.get("characterID1", "").strip()
            char2_id = row.get("characterID2", "").strip()
            
            if character_id == char1_id or character_id == char2_id:
                utterances = row.get("utterance", {}).get("text", [])
                # Clean up the texts which sometimes have trailing spaces or formats
                cleaned_utterances = [str(u).strip() for u in utterances if str(u).strip()]
                if cleaned_utterances:
                    dialogues.append(cleaned_utterances)

        return dialogues
