<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Instead of counting HTTP requests (everything is often one POST to `/graphql`), dumps assign each field a cost, sum the query, and reject over a budget. Nested lists multiply cost. Used for rate limiting and DoS control together with max depth, timeouts, and pagination.

Libraries named in compilations: graphql-depth-limit, graphql-query-complexity. Query complexity is described as GraphQL's answer to REST-style per-URL rate limits.

> [!warning] Unverified traps from the dump
> - Dump claim: rate-limit by cost, not by request count, because one GraphQL document can be huge.
