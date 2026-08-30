<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump pattern: OncePerRequestFilter reads Authorization, builds a custom Authentication, optionally authenticates via AuthenticationProvider, then sets SecurityContextHolder.

Add the filter before UsernamePasswordAuthenticationFilter. Pair with SessionCreationPolicy.STATELESS and often csrf().disable() for a pure token API.
> [!warning] Unverified traps from the dump
> - Setting Authentication in the filter without validating the token is a forged-header hole.
> - Do not leave form login + sessions on if you meant a bearer-only API.
