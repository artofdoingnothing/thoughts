# Backend AI Thought Generation & Persona Derivation

**Status:** COMPLETED

## Context / Current State

The core feature is taking a set of selected movie characters, extracting their dialogues, generating unique thoughts, and synthesizing a brand new `Persona` from this data. This crosses multiple domains: AI Processing, Thought Management, and Persona Management.

## Action Items

- [x] Create a new Use Case to handle the generation request containing the user's selected characters.
- [x] For each selected character, randomly extract 100 dialogues from the `cornell_movie_dialog` dataset.
- [x] Invoke the AI Processing domain to generate 5 distinct `Thoughts` from the 100 dialogues for each character. Ensure the LLM prompt enforces a structured JSON response.
- [x] Store these newly generated `Thoughts` via the Thought Management domain.
- [x] Invoke the AI Processing domain again to synthesize a new `Persona` profile based on the entire collection of newly generated thoughts. The AI must auto-fill/guess missing information (name, age, gender, profile). Ensure the LLM prompt returns structured JSON.
- [x] Save the newly derived `Persona` via the Persona Management domain, and link the generated thoughts to this new persona's `persona_id`.

## Additional Notes

- This process will be long-running. Avoid blocking the HTTP response; process it asynchronously via background workers and the domain event bus.
- Update tests for the newly created Use Cases and Workers.
