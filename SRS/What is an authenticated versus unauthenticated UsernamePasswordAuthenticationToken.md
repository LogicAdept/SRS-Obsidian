<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump form-login internals: the filter first builds an unauthenticated UsernamePasswordAuthenticationToken (credentials present, not yet trusted). After AuthenticationManager succeeds, a new authenticated token (principal + authorities, credentials often erased) goes into SecurityContext.
> [!warning] Unverified traps from the dump
> - Reusing the unauthenticated token as authenticated without going through the manager skips PasswordEncoder.matches.
