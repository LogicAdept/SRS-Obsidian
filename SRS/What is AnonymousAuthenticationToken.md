<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: AnonymousAuthenticationFilter puts an AnonymousAuthenticationToken in the context so later filters never see null Authentication. Principal is anonymousUser; authority ROLE_ANONYMOUS. isAuthenticated() is true on that token in dumps — a trick question.
> [!warning] Unverified traps from the dump
> - isAnonymous() / checking the token type is the dump way to detect it, not authentication == null.
