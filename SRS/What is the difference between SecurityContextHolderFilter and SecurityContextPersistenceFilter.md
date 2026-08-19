<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Older dumps name SecurityContextPersistenceFilter: store SecurityContext between HTTP requests and clear SecurityContextHolder when the request finishes.

Security 6 interview lists put SecurityContextHolderFilter at that slot instead: load from SecurityContextRepository at the start, save at the end. Same job, newer type in the default chain.
> [!warning] Unverified traps from the dump
> - Both clear ThreadLocal at the end of the request. Forgetting that is why a pooled thread can leak another user’s Authentication.
