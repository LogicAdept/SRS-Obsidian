<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Context is a per-request object built once when the request arrives and passed as the third resolver argument. Dumps put the authenticated user, db handles, and DataLoaders there.

Typical setup: a `context` function reads HTTP headers/cookies, verifies a token, attaches `context.user`, and creates fresh loaders. Resolvers must not share one DataLoader across requests: dumps say that leaks user A's cached rows to user B.

> [!warning] Unverified traps from the dump
> - Dump claim: create context and DataLoaders per request; never reuse the loader cache across users.
