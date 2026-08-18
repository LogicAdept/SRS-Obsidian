<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

REST can limit per route: `GET /users` is one kind of load. GraphQL dumps: everything may share one route, so request-counting does not distinguish a cheap `{ __typename }` from a deep nested list.

Need operation-name metrics, cost/complexity budgets, depth limits, and sometimes alias/batch caps. Per-endpoint HTTP 429 on `/graphql` treats a tiny and a huge document as equals.

> [!warning] Unverified traps from the dump
> - Dump claim: instrument per operation name / resolver, not per URL.
