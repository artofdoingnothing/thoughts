# Rewrite Conversation Generator to React Query

**Status:** COMPLETED

## Context / Current State

- `conversations` and `personas` are fetched natively using `useEffect` and `axios`.
- Polling for `generateMessage` and `generateSequence` is hacked together using multiple `setTimeout` calls (`setTimeout(fetchConversations, 2000)`, etc.).
- State updates lack comprehensive loading/error states out of the box.

## Action Items

### Queries (`useQuery`)

- Create a hook `useConversations()` using `useQuery({ queryKey: ['conversations'], queryFn: ... })`.
- Create a hook `usePersonas()` using `useQuery({ queryKey: ['personas'], queryFn: ... })`.

### Mutations (`useMutation`)

- `createConversation`: on success, `queryClient.invalidateQueries({ queryKey: ['conversations'] })`.
- `endConversation`: on success, invalidate conversations query.
- `addPersona`: on success, invalidate conversations query.

### Polling Strategy for Generation (`useMutation` + `useQuery`)

- For `generateMessage` and `generateSequence`, the current method calls API and tries to refetch after 2s, 5s, 8s.
- **Improved Approach**: After triggering a generation mutation, enable a temporary `refetchInterval` on the conversations query, or track the specific conversation's status (if the API supports a `status` endpoint). If no task status API exists, simply set `refetchInterval: 2000` on `useConversations` for a fixed duration or until a certain condition is met to utilize React Query's native polling.

## Additional Notes

### Cleanup

- Remove local state `conversations` and `personas`.
- Remove `setTimeout` hacks.
- Replace manual error logging and catch blocks with `onError` callbacks in mutations.
