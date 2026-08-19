<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: AccessDeniedHandler runs when an authenticated user fails authorization (AccessDeniedException). Default is 403. Customizing the access-denied page wires this (or a 403 view), not AuthenticationEntryPoint.
> [!warning] Unverified traps from the dump
> - Anonymous 403s are usually converted to an authentication entry-point challenge, so your AccessDeniedHandler never sees them.
