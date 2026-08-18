<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

DataLoader sits between resolvers and the store. `load(key)` during one event-loop tick is queued; a batch function receives all keys and must return results in the same order. Within that loader's lifetime, a key is fetched once (memoized promise).

Create a **new** DataLoader per request so cache never leaks across users. Net effect dumps advertise: N+1 collapses and duplicate IDs de-duplicate.

```
author: (post) => userLoader.load(post.authorId)
```

> [!warning] Unverified traps from the dump
> - Dump claim: batch function order must match the keys array or the wrong objects attach to parents.
