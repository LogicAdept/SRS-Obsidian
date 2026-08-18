<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Introspection is querying the schema itself via reserved meta-fields such as `__schema`, `__type`, and `__typename`. The type system comes back as data: types, fields, arguments, directives.

Dumps say it powers GraphiQL / Apollo Sandbox, codegen, and schema validation or diffing in CI. It is often disabled or gated in production so attackers do not get a full map of experimental or sensitive fields. That is reduced exposure, not authorization: dumps still say enforce auth per field.

> [!warning] Unverified traps from the dump
> - Dump claim: many teams keep introspection behind auth or only in staging and publish a schema artifact to trusted clients.
