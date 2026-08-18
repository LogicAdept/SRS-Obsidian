<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Directives are `@` annotations on schema definitions or executable documents.

- `@deprecated` (schema): marks a field or enum value obsolete with an optional reason; tooling warns; the field still works.
- `@include(if: Boolean)` (executable): include a field or fragment only when true.
- `@skip(if: Boolean)` (executable): omit when true. Dumps say if both apply, `@skip` wins.

`@include` / `@skip` let one query adapt to runtime variables instead of shipping multiple query variants. Lists also mention custom directives for auth, logging, or formatting.

> [!warning] Unverified traps from the dump
> - Dump claim: putting `@deprecated` on a field inside a client query (as some examples do) is schema-side, not a client execution directive.
