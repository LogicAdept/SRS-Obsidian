<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @PostFilter runs the method, loads the full collection, then drops elements in memory. A large query still hits the database. Prefer filtering in the query (or SecurityEvaluationContextExtension) when the list is huge.
> [!warning] Unverified traps from the dump
> - Denial of a single forbidden row still paid for loading every row.
