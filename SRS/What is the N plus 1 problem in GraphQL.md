<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Resolvers run per field per object. Fetch a list of N posts (1 query), then each `author` resolver hits the DB once: N more queries. That is 1 + N hits. Dumps call it the common GraphQL performance bug.

DataLoader (same lists) is the usual fix: `loader.load(id)` buffers IDs in one tick, then one `WHERE id IN (...)` batch. Result: list query plus one batched relation query.

> [!warning] Unverified traps from the dump
> - Dump claim: GraphQL does not batch by itself; naive nested resolvers always N+1.
