# Rewrite Essay Generator to React Query

**Status: COMPLETED**

## Current State

- `personas` are fetched natively using `useEffect` and `axios`.
- Polling for the background task is handled using `window.setInterval` within a `useEffect`, checking the `jobId` and updating states locally.
- Managing multiple loading and error states manually.

## React Query Hooks Migration Plan

1. **Queries (`useQuery`)**:
   - `usePersonas()` using `useQuery({ queryKey: ['personas'], queryFn: fetchPersonas })`.
   - `useEssayStatus(jobId)` using `useQuery({ queryKey: ['essayStatus', jobId], queryFn: () => getStatus(jobId) })`

2. **Refactoring Polling for Generation Status (`refetchInterval`)**:
   - Instead of manual `window.setInterval`, leverage React Query's `refetchInterval` on `useEssayStatus(jobId)`:
     ```typescript
     useQuery({
       queryKey: ["essayStatus", jobId],
       queryFn: () =>
         axios
           .get(`${API_BASE_URL}/essay/status/${jobId}`)
           .then((res) => res.data),
       enabled: !!jobId,
       refetchInterval: (data) =>
         data?.status === "finished" || data?.status === "failed"
           ? false
           : 2000,
     });
     ```
   - Watch the data from `useEssayStatus` directly to show the generated essay or error states instead of sinking state to local `generatedEssay` and `error` `useState`.

3. **Mutations (`useMutation`)**:
   - `generateEssay` mutation triggers the POST request.
   - On mutation success, capture the returning `jobId` and store it in regular `useState` to enable the `useEssayStatus` query to begin polling.

4. **Cleanup**:
   - Remove `setTimeout`/`setInterval` implementations.
   - Remove redundant `isGenerating` state, because React Query's `isLoading` or `isFetching` properties provide this intrinsically.
