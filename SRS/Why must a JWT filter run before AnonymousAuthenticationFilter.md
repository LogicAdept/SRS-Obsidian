<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump placement table: if your JWT filter runs after AnonymousAuthenticationFilter, an anonymous Authentication is already in SecurityContextHolder and the token is ignored. Place custom auth before UsernamePasswordAuthenticationFilter (and thus before anonymous).
> [!warning] Unverified traps from the dump
> - AuthorizationFilter then sees anonymous and returns 401/403 even with a valid Bearer header.
