<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the anonymous authentication filter assigns ROLE_ANONYMOUS to unauthenticated callers (on by default). Prefer isAnonymous() over checking that role name.

Disabling anonymous authentication leaves Authentication null instead of an anonymous token.
> [!warning] Unverified traps from the dump
> - permitAll allows anonymous; authenticated() does not. Mixing those two is the usual 401 on ‘public’ pages.
