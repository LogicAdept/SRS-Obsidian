<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump list:

- Authentication — who the user is.
- Authorization — what they may do.
- SecurityContextHolder — current thread’s security details.
- AuthenticationManager — runs authentication.
- AccessDecisionManager — access-control decision (older dumps).
- GrantedAuthority — roles or permissions.

Newer dumps swap AccessDecisionManager for AuthorizationManager / AuthorizationFilter.
> [!warning] Unverified traps from the dump
> - This is a map of types, not a substitute for the filter-chain order question.
