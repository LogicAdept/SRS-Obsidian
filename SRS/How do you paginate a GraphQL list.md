<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Two dump models.

Offset: `limit` / `offset` (or page size). Maps to SQL LIMIT/OFFSET. Simple; can jump to page N. Drifts when rows insert/delete (skips/duplicates); large offsets are slow.

Cursor / Relay: opaque cursor on a row; `first`/`after` or `last`/`before`. Stable under concurrent writes; fits infinite scroll. Cannot easily jump to page 17.

Relay Connection shape: `edges { node, cursor }` plus `pageInfo { hasNextPage, endCursor }`. Lists say you can use that shape without Relay the client.

> [!warning] Unverified traps from the dump
> - Dump claim: cursor pagination is preferred for large or fast-changing lists; offset is fine for small stable data.
