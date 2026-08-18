<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump comparison: GraphQL is a query language and runtime where the client names fields against a typed schema, typically through one endpoint whose response shape follows the query. REST uses many fixed resource URLs; the server defines each endpoint's payload.

Client-driven vs server-driven: REST endpoints return a fixed shape; GraphQL clients declare fields. Nested selections can fetch related data in one round trip instead of `/users/1` then `/users/1/posts`.

Tradeoff named in dumps: REST leans on HTTP caching and simple status codes; GraphQL trades that for flexible fetching, then needs application-level caching, query cost limits, and resolver care.

> [!warning] Unverified traps from the dump
> - Dump claim: 'one endpoint' is the usual hosting model, not a language requirement.
> - Over-fetching can reappear in resolvers that still load unused columns.
