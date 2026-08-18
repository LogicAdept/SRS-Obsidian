<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If you omit a resolver, dumps describe a default: read `parent[fieldName]` (in JS reference implementations, `parent.name` for field `name`). If the property is a function, it is called with the field's args and context. If missing, the field is null (or errors if non-null).

Why: most object fields just expose properties already on the fetched object. Override when the field is computed, the property name differs, or you need another fetch (relations, other services).

> [!warning] Unverified traps from the dump
> - Dump claim: default resolvers are a convenience of implementations, not a separate GraphQL type.
