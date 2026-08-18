<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Three operation types. Query reads data; root fields are expected to be side-effect free and may resolve in parallel. Mutation writes data (create/update/delete); top-level fields execute serially so writes do not race; dumps say it often returns the affected data for cache updates. Subscription streams: a long-lived connection (often WebSockets) pushes a new result when a server-side event fires.

Only Query is mandatory in the schema. Mutation and subscription roots are optional object types, distinct from Query if present.

> [!warning] Unverified traps from the dump
> - Dump claim: a query *can* still write; mutation-for-writes is convention plus serial root execution, not a language ban.
