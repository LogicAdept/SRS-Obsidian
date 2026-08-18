<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A GraphQL schema is the strongly typed definition of every type, field, and operation the API supports. Dumps call it a contract: it specifies what the client can ask for and what the server promises to return.

It typically contains object types, scalars, enums, input types, and the root Query / Mutation / Subscription entry points. Queries are validated against it before execution. Introspection lets tools autocomplete, generate types, and render docs (for example GraphiQL).

Every GraphQL server is described as having two core parts: a schema and resolve functions. The schema models what can be fetched and how types relate.

> [!warning] Unverified traps from the dump
> - Dump claim: additive schema changes are usually non-breaking; schema-diff tools flag breaking ones.
> - Only the query root is mandatory; mutation and subscription roots are optional.
