# Rewrite Thoughts Page to React Query

**Status:** COMPLETED

## Context / Current State

- Native implementation of pagination, filters, and loading using `useState` and `useEffect`.
- State is tightly coupled with `fetchThoughts` which must be passed a complex dependency array `[page, selectedTag, selectedEmotion, selectedPersona]`.
- Prop-drilling `refreshKey` from an unknown source to force updates.

## Action Items

### Queries (`useQuery`)

- Build a robust `useThoughts({ page, tag, emotion, persona_id })` query hook incorporating all pagination and filters in the `queryKey`: `['thoughts', { page, tag, emotion, personaId }]`.
- Setup `keepPreviousData: true` (or `placeholderData: keepPreviousData` in v5) to enable smooth pagination transitions without violent loading spinners on each page change.
- Swap `useEffect` fetching of `personas` to the generic `usePersonas()` react query hook.

### Mutations (`useMutation`)

- Implement `useDeleteThought()` mutation. Once successfully deleted, trigger `queryClient.invalidateQueries({ queryKey: ['thoughts'] })`. Can implement optimistic updates if preferred.

## Additional Notes

### Cleanup

- `refreshKey` prop becomes obsolete, invalidate queries generically on any global updates.
- Remove deeply complex `useEffect` implementations relying on native state sync.
- Relieve `loading` state to use native React Query `isLoading` and `isFetching`.
