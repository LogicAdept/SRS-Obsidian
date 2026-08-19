<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump filter list (early in the chain): SecurityContextPersistenceFilter loads SecurityContext from the repository (usually the HTTP session) at the start of the request and clears SecurityContextHolder at the end so thread pools do not leak users.

Spring Security 6 dumps also name SecurityContextHolderFilter as the successor. STATELESS skips writing the context to the session.
> [!warning] Unverified traps from the dump
> - Clearing at request end is why ThreadLocal must not be assumed after the response; worker threads need explicit propagation.
