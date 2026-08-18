<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Both compose many GraphQL services into one schema.

Schema stitching: a gateway merges remote schemas and you write delegation / type-merging in the gateway. Glue is central.

Apollo Federation (dumps): each subgraph declares ownership and extensions with directives (`@key`, `@external`, `@requires`). A router composes a supergraph. A subgraph can extend a type defined elsewhere; `_entities` reference resolvers fetch across services.

Why move: team autonomy, less brittle central glue, schema checks and a supergraph artifact.

> [!warning] Unverified traps from the dump
> - Dump follow-up: how a type is extended across services — entity `@key`.
