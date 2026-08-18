<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump downsides: HTTP/CDN caching is harder; unbounded nested queries and N+1; schema/resolver/tooling overhead; file/binary uploads need extra specs; learning curve; server does more parse/validate work; queries can be larger than a simple REST GET.

Recommend against (same lists) when the API is simple CRUD, you rely heavily on HTTP caching, or you mostly serve files. REST is called simpler and cheaper there. GraphQL helps when many clients need different slices of a connected graph.

> [!warning] Unverified traps from the dump
> - Dump claim: GraphQL is not a free upgrade; it moves complexity onto the server.
