<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A resolver produces the value for one field. Dumps list four arguments, in order:

1. `parent` (also root/source): result of the parent field's resolver.
2. `args`: arguments from the query (for example `id` in `user(id: 5)`).
3. `context`: per-request shared state (user, db, DataLoaders).
4. `info`: execution metadata (AST, field name, path, schema).

A resolver may return a value or a Promise; the engine awaits it before children. The return value becomes `parent` for nested resolvers.

> [!warning] Unverified traps from the dump
> - Dump claim: names vary (`obj` vs `parent`) but the four slots are the same in common JS servers.
