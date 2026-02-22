# Backend Dataset Integration & Search API

**Status:** COMPLETED

## Context / Current State

Currently, the system generates thoughts from blogs. We are shifting to generating thoughts from movie characters' dialogue using the `cornell_movie_dialog` dataset on Hugging Face. The Presentation Layer needs backend support to query this dataset.

## Action Items

- [x] Create a service in the backend to interact with or download the `cornell_movie_dialog` dataset from Hugging Face.
- [x] Implement an API endpoint under a suitable router to search for movies and characters.
- [x] The search endpoint must support filtering by: movie genre, IMDB rating, and release year.
- [x] The search endpoint must support a wildcard search string on the movie title.
- [x] Return structured JSON responses containing character details appropriate for the Presentation Layer.

## Additional Notes

- Ensure the dataset querying is efficient (consider local caching, a persistent local database table, or vector DB if querying Hugging Face directly is too slow).
- Follow the Data Integration / External Services patterns within the DDD structure. Update the domain documentation if a new domain pattern emerges.
- Remember to add tests for the new endpoint and service.
