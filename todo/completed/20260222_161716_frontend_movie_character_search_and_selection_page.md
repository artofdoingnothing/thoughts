# Frontend Movie Character Search & Selection Page

**Status:** COMPLETED

## Context / Current State

We need a dedicated UI for users to build a roster of movie characters from the `cornell_movie_dialog` dataset. This involves searching the new backend dataset API and managing a local selection state before triggering persona generation.

## Action Items

- [x] Create a new page component in the Presentation Layer for Movie Character Search.
- [x] Implement a two-column layout: Left side for "Selected Characters List", Right side for "Search & Results".
- [x] On the right side, add search inputs for: Wildcard Title, Genre, IMDB Rating, and Year.
- [x] Render search results fetched from the backend on the right side.
- [x] Add functionality to select a character from the search results (right) and move them to the selected list (left).
- [x] Allow removing characters from the selected list.

## Additional Notes

- Utilize React Query for fetching data from the new backend search API, consistent with recent refactoring efforts in the frontend.
- Follow frontend code instructions for styling and state management.
- Ensure the selected characters state is correctly managed locally before submission.
