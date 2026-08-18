<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Variables are typed placeholders declared on the operation (`query GetUser($id: ID!)`) and supplied in a separate JSON variables map, referenced as `$id`. Dumps prefer them over stuffing values into the query string so the query text stays static.

Claimed benefits: reuse and caching/persisted queries by hash; server validates types and non-null rules; no string-concatenation of user values (dumps call this avoiding injection-style bugs); no manual escaping of strings, enums, or input objects.

Anonymous shorthand queries cannot declare variables; named operations are required for variables in those lists.

> [!warning] Unverified traps from the dump
> - Dump claim: never build query strings by interpolating user input; pass a variables map instead.
