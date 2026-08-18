<!--
reps: 0
priority: 0
-->
#API/GraphQL #Networking/Web/Protocols/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Subscriptions are the third operation type: the client selects fields like a query but receives a **stream** of results when events fire (chat message, status). Dumps: usually a persistent connection; common transport is WebSockets (`graphql-ws`); SSE is listed for one-way streams. Under the hood, publish to pub/sub; the subscription resolver listens.

WebSockets are the raw transport; subscriptions are the GraphQL feature (schema, validation, field selection) that often rides on WebSockets. Vs polling: push on change instead of timed re-query.

Skip subscriptions when updates are rare: polling is simpler and avoids persistent-connection ops.

> [!warning] Unverified traps from the dump
> - Dump claim: GraphQL-over-SSE is sometimes recommended when you do not need bidirectional sockets.
