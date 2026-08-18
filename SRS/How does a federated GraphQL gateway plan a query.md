<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/Gateway #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the gateway/router is the only client-facing entry. It exposes the composed supergraph, **plans** the query into subgraph steps, executes those sub-requests (including entity references), and merges one response matching the query.

Also listed at the router: auth, rate limiting, caching, tracing. `@apollo/gateway` (Node) vs Apollo Router (Rust) are named as the same role, different runtime. It is a shared bottleneck: its uptime bounds the graph.

A supergraph is the unified schema from subgraphs; types can be split (User profile vs orders) linked by `@key`.

> [!warning] Unverified traps from the dump
> - Dump claim: clients never talk to subgraphs directly in this architecture.
