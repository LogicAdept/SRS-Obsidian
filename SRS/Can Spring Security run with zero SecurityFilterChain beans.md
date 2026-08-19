<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Yes — if FilterChainProxy’s list is empty, every request passes through with no security filters. @EnableWebSecurity auto-configures a default chain, so you would have to remove that on purpose.
> [!warning] Unverified traps from the dump
> - Zero chains is not the same as permitAll() inside a chain. permitAll still runs CsrfFilter, HeaderWriterFilter, CORS, and the rest.
