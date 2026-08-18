<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Query root fields: dumps say parallel, because reads are treated as side-effect free. Mutation root fields: serial, in document order, so the first write finishes before the next starts (example: `createUser` then `updateUser` in one operation).

Nuance in the same dumps: serial applies to **root** mutation fields only. Nested resolvers under each mutation still run in parallel, like queries.

> [!warning] Unverified traps from the dump
> - Dump claim: parallel query roots are an optimization; if a query resolver writes, that optimization becomes a bug.
