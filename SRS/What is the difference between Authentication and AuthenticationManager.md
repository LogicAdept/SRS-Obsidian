<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump table:

- Authentication — the object: principal, credentials, authorities; present before (unauthenticated token) and after login.
- AuthenticationManager — the process: authenticate() delegates to AuthenticationProvider and returns a populated Authentication or throws.

You do not ‘store the manager in the context’. You store Authentication in SecurityContext.
> [!warning] Unverified traps from the dump
> - Calling getAuthentication() null vs unauthenticated token is a different bug from a missing AuthenticationManager bean.
