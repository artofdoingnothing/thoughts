# Rewrite Personas Page to React Query

**Status: COMPLETED**

## Current State

- `personas` are fetched statically using `useEffect` and `fetch`.
- `fetchPersonas` is re-called manually in subcomponents and inside `handleSuccess` callbacks. Prop-drilling of completion handlers to modals.
- Reloading the page fully triggers a manual fetch of the persona list instead of using a cached or synchronized store.

## React Query Hooks Migration Plan

1. **Queries (`useQuery`)**:
   - Retrieve all personas via `hooks/usePersonas.ts`: `useQuery({ queryKey: ['personas'], queryFn: ... })`.
   - Access this hook from any component (e.g., `PersonasPage` or modals) natively without prop-drilling.

2. **Mutations (`useMutation`)**:
   - Modify `handleRegenerate` into a dedicated mutation `useRegeneratePersona()`. On `onSuccess: () => queryClient.invalidateQueries({ queryKey: ['personas'] })`.
   - Modal Actions:
     - Update `CreatePersonaModal` with a `useCreatePersona` mutation, simplifying prop-drilling `handleSuccess`.
     - Update `DerivePersonaModal` with a `useDerivePersona` mutation.
   - Using mutations directly lets the child components invalidate the global cache, reducing tight coupling and redundant API fetches.

3. **Cleanup**:
   - Eliminate explicit `handleSuccess` props from `CreatePersonaModal` and `DerivePersonaModal`. Use `onSuccess` on component unmount or let mutations invalidate the `['personas']` query instantly.
   - Remove the custom `fetchPersonas` refetchings logic.
