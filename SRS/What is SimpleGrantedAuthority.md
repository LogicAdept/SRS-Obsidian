<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump UserDetails examples: SimpleGrantedAuthority("ROLE_ADMIN") is the usual GrantedAuthority implementation — a string. hasRole("ADMIN") looks for ROLE_ADMIN on that string.
> [!warning] Unverified traps from the dump
> - Storing authority ADMIN (no prefix) and then hasRole("ADMIN") fails because hasRole prepends ROLE_.
