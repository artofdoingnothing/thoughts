# Frontend Trigger Persona Generation from Characters

**Status:** COMPLETED

## Context / Current State

Once a user has selected a list of movie characters on the new page, they need a way to initiate the generation process and view the resulting AI-derived Persona.

## Action Items

- [x] Add a "Generate Persona" action button to the bottom of the "Selected Characters List" (left side) on the Character Search page.
- [x] Connect this button to a React Query mutation that calls the backend generation endpoint with the selected character data.
- [x] Implement graceful loading states, progress indicators, or polling (using `refetchInterval`) since this involves background AI processing.
- [x] Once generation is complete and the new Persona is ready, either redirect the user to the newly created Persona's detail page or display the new Persona and its generated thoughts in a clean UI component.

## Additional Notes

- Handle any potential generation errors gracefully in the UI.
- Use structured JSON parsing if interacting directly with the generation response, but rely on React Query for standard API states.
