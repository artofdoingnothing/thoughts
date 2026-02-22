# Movie Dataset Direct Download Tasks

---

id: TASK-1
title: Download Cornell dataset automatically in Docker container builds
type: chore
priority: high
status: done
created_by: task-creator-agent
created_at: 2026-02-22T18:35:00Z
assignee: unassigned
bounded_context: Infrastructure
layer: infrastructure
estimated_effort: S
depends_on: [none]
blocks: [TASK-2]

---

## Summary

The Cornell movie dialogs dataset is currently fetched dynamically from Hugging Face at runtime, which can cause network delays and dependency issues. This task moves the dataset fetching step to the Docker build process so the raw dataset files are burned into the application and worker images.

## Background and Context

The `backend/Dockerfile` and `workers/Dockerfile` currently only install pip dependencies. The dataset needs to be manually downloaded from `http://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip` and unzipped into a known directory within the container (e.g., `/app/data/cornell_dialogs`) during the `docker build` phase so the files are locally available for the application.

## Acceptance Criteria

1. The `backend/Dockerfile` must contain a RUN instruction to download the `.zip` file from the Cornell server.
2. The downloaded `.zip` file must be extracted into a directory accessible by the app (e.g., `/app/data/cornell_dialogs/cornell movie-dialogs corpus`).
3. The original `.zip` file must be removed after extraction to keep the image size minimal.
4. The exact same steps must be applied to `workers/Dockerfile`.
5. The container must build successfully and contain the `movie_lines.txt`, `movie_conversations.txt`, `movie_titles_metadata.txt`, and `movie_characters_metadata.txt` files.

## DDD Considerations

N/A - Pure infrastructure and deployment concern.

## Documentation Requirements

Update the README section on running locally to denote where dataset files are stored, as well as if any manual steps are needed if developers want to run without Docker.

## Out of Scope

Refactoring the python code to use these new files.

## Open Questions

- Can the files be downloaded on developers' host machines seamlessly without Docker? Or should a helper script be defined for local non-Docker development? (To be decided during implementation).

## Definition of Done

- [x] All acceptance criteria are met.
- [x] Tests are added or updated.
- [x] Documentation requirements are fulfilled.
- [x] Code review approved by at least one domain expert.
- [x] No broken bounded context contracts.
- [x] Task status updated to `done`.

---

id: TASK-2
title: Refactor MovieDatasetService to use local dataset files
type: refactor
priority: high
status: done
created_by: task-creator-agent
created_at: 2026-02-22T18:35:00Z
assignee: unassigned
bounded_context: DatasetService
layer: infrastructure
estimated_effort: M
depends_on: [TASK-1]
blocks: [none]

---

## Summary

Refactor the existing `MovieDatasetService` to read directly from the locally downloaded Cornell dataset files instead of streaming from the Hugging Face `datasets` library. This allows processing custom features that the Hugging Face library stream doesn't easily afford.

## Background and Context

Currently, `libs/dataset_service/movie_dataset_service.py` uses `load_dataset("cornell_movie_dialog", split="train", streaming=True)`. We need to switch this logic to parse the `txt` files downloaded by TASK-1.

The dataset uses `+++$+++` as a delimiter.
The files of interest include:

- `movie_titles_metadata.txt` for `movieID`, title, year, IMDB rating, and genres.
- `movie_characters_metadata.txt` for mapping `characterID`, character name, and `movieID`.
- `movie_lines.txt` for `lineID`, `characterID`, and the text of the line.
- `movie_conversations.txt` for mapping a sequence of `lineID`s that make up a continuous dialogue.

## Acceptance Criteria

1. The `datasets` library import must be removed from `libs/dataset_service/movie_dataset_service.py`.
2. `MovieDatasetService.search_characters(...)` must manually parse the `movie_titles_metadata.txt` and `movie_characters_metadata.txt` to find matching movies and characters, returning the exact same `List[dict]` response shape.
3. `MovieDatasetService.get_character_dialogues(...)` must parse the `movie_conversations.txt` and `movie_lines.txt` to reconstruct dialogues for a given `character_id`. It must return the exact same `List[List[str]]` signature.
4. The service should parse efficiently to avoid excessive memory usage where possible (e.g. generator patterns, read-by-line, or reasonable caching).
5. The API routes and Workers that depend on `MovieDatasetService` must continue to behave identically, running successfully against this new implementation.

## DDD Considerations

`MovieDatasetService` acts as an Infrastructure service, providing data to components. Implementing this change respects the current interface so it will not break consumers.

## Documentation Requirements

N/A - Implementation detail change only.

## Out of Scope

Modifying the output schema of the `MovieDatasetService` methods.

## Open Questions

- Will loading all lines into memory at once cause memory spikes in the Docker container? Consider lazy loading or line-by-line streaming.

## Definition of Done

- [x] All acceptance criteria are met.
- [x] Tests are added or updated.
- [x] Documentation requirements are fulfilled.
- [x] Code review approved by at least one domain expert.
- [x] No broken bounded context contracts.
- [x] Task status updated to `done`.
