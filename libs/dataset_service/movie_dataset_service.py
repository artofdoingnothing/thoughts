import os
import ast
from typing import List, Optional


class MovieDatasetService:
    def __init__(self, data_dir: str = "/dataset/cornell_dialogs"):
        self.data_dir = data_dir
        # Check if the files are nested in the unzipped folder
        nested_dir = os.path.join(self.data_dir, "cornell movie-dialogs corpus")
        if os.path.exists(nested_dir) and os.path.exists(os.path.join(nested_dir, "movie_titles_metadata.txt")):
            self.data_dir = nested_dir
        
        # For local development outside docker
        fallback_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/cornell_dialogs"))
        if not os.path.exists(os.path.join(self.data_dir, "movie_titles_metadata.txt")) and os.path.exists(fallback_dir):
            self.data_dir = fallback_dir

    def _parse_line(self, line: str) -> List[str]:
        return [part.strip() for part in line.split("+++$+++")]

    def search_characters(
        self,
        title_query: Optional[str] = None,
        genre: Optional[str] = None,
        min_imdb_rating: Optional[float] = None,
        release_year: Optional[str] = None,
        character_name: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        titles_file = os.path.join(self.data_dir, "movie_titles_metadata.txt")
        characters_file = os.path.join(self.data_dir, "movie_characters_metadata.txt")

        # Fallback to empty if not exists (for tests)
        if not os.path.exists(titles_file) or not os.path.exists(characters_file):
            return []

        # Read movies
        valid_movies = {}
        with open(titles_file, "r", encoding="iso-8859-1") as f:
            for line in f:
                parts = self._parse_line(line)
                if len(parts) >= 6:
                    movie_id, title, year, rating_str, votes, genres_str = parts[:6]
                    
                    if title_query and title_query.lower() not in title.lower():
                        continue
                        
                    try:
                        movie_genres = ast.literal_eval(genres_str)
                    except:
                        movie_genres = []
                        
                    if genre and genre.lower() not in [g.lower() for g in movie_genres]:
                        continue
                        
                    if release_year and release_year != year:
                        continue
                        
                    if min_imdb_rating is not None:
                        try:
                            rating = float(rating_str)
                            if rating < min_imdb_rating:
                                continue
                        except ValueError:
                            continue
                            
                    valid_movies[movie_id] = {
                        "movie_id": movie_id,
                        "movie_title": title,
                        "movie_year": year,
                        "movie_imdb_rating": rating_str,
                        "movie_genres": movie_genres,
                    }

        if not valid_movies:
            return []

        # Read characters
        results = []
        with open(characters_file, "r", encoding="iso-8859-1") as f:
            for line in f:
                parts = self._parse_line(line)
                if len(parts) >= 4:
                    char_id, char_name, movie_id, movie_title = parts[:4]
                    if movie_id in valid_movies:
                        if character_name and character_name.lower() not in char_name.lower():
                            continue
                        movie_info = valid_movies[movie_id]
                        results.append({
                            **movie_info,
                            "character_id": char_id,
                            "character_name": char_name,
                        })
                        if len(results) >= limit:
                            break

        return results

    def get_character_dialogues(self, character_id: str, limit: int = 100) -> List[List[str]]:
        conversations_file = os.path.join(self.data_dir, "movie_conversations.txt")
        lines_file = os.path.join(self.data_dir, "movie_lines.txt")

        if not os.path.exists(conversations_file) or not os.path.exists(lines_file):
            return []

        # Find conversations involving the character
        conv_line_ids = []
        with open(conversations_file, "r", encoding="iso-8859-1") as f:
            for line in f:
                parts = self._parse_line(line)
                if len(parts) >= 4:
                    char1_id, char2_id, movie_id, lines_str = parts[:4]
                    if character_id == char1_id or character_id == char2_id:
                        try:
                            line_ids = ast.literal_eval(lines_str)
                            conv_line_ids.append(line_ids)
                        except:
                            pass
                if len(conv_line_ids) >= limit:
                    break
        
        if not conv_line_ids:
            return []
            
        # Collect all required line IDs to avoid scanning multiple times
        required_line_ids = set()
        for c in conv_line_ids:
            required_line_ids.update(c)
            
        # Parse lines
        lines_map = {}
        with open(lines_file, "r", encoding="iso-8859-1") as f:
            for line in f:
                parts = self._parse_line(line)
                if len(parts) >= 5:
                    line_id = parts[0]
                    if line_id in required_line_ids:
                        text = parts[-1]
                        lines_map[line_id] = text

        dialogues = []
        for c in conv_line_ids:
            dialogue = []
            for line_id in c:
                if line_id in lines_map:
                    dialogue.append(lines_map[line_id])
            if dialogue:
                dialogues.append(dialogue)

        return dialogues
