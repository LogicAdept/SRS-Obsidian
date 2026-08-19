<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump (also ExceptionTranslationFilter one-liner): AuthenticationException means not authenticated (or auth failed) → 401 / login challenge. AccessDeniedException from an already-authenticated user → 403. AccessDeniedException from anonymous is treated like 401 (challenge).
> [!warning] Unverified traps from the dump
> - Method security throws AccessDeniedException, not AuthenticationException, when a logged-in user fails @PreAuthorize.
