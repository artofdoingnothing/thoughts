# Rewrite Thought Generator to React Query

**Status:** COMPLETED

## Context / Current State

- Fetches `personas` via `useEffect`.
- Submits `generate-thoughts` mutation using manual `axios.post`.
- State updates lack robust loading/error feedback integration out of the box outside of manually managing `setMessage()`.

## Action Items

### Queries (`useQuery`)

- Hook into the same `usePersonas()` hook created for other pages instead of duplicating API fetches.

### Mutations (`useMutation`)

- Provide a `useGenerateThoughts()` wrapper over the endpoint using `useMutation`.
- Utilize React Query mutation states (`isPending`, `isSuccess`, `isError`) directly in the UI component to conditionally disable buttons and display messages instead of manual error catch blocks.
- Trigger a global toast or status message within `onSuccess` or `onError`.

## Additional Notes

### Cleanup

- Remove API base URL constants duplicated across pages (move into an Axios instance / Query Function layer).
- Drop the explicit `useEffect` fetching logic for `personas`.
