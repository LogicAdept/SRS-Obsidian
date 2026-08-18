<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump pipeline: parse the document to an AST; validate against the schema (fields exist, types match, required args present); execute by walking the selection, calling resolvers field by field; assemble `data` / `errors` (often JSON).

Execution is top-down and depth-first along the query tree. A field's result becomes `parent` for children. Sibling fields at one level may run in parallel. Query root fields: parallel. Mutation root fields: serial. Invalid queries die in validation before resolvers or DB calls.

Cost limits and DataLoader batching hook into execution, not parse.

> [!warning] Unverified traps from the dump
> - Dump claim: validation should run before any resolver; memoizing a previously validated document is a listed exception in some texts.
