<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Clients can nest selections arbitrarily. Dumps stack defenses: cap **depth** (reject nesting past N), **complexity/cost** (weight fields, reject over budget), timeouts, paginate every list so nothing is unbounded.

For public APIs, persisted-query allowlists so arbitrary expensive shapes never run. Same lists mention rate limits and alias/batch caps against amplification.

> [!warning] Unverified traps from the dump
> - Dump claim: depth limit alone is not enough; a wide cheap-looking query can still be expensive — that is cost analysis.
