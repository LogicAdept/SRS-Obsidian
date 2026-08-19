<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**401 Unauthorized:** authentication failed or is missing — Spring Security does not know who you are (no/invalid credentials).

**403 Forbidden:** you are authenticated but not allowed — authorization failed (missing role/authority).

`ExceptionTranslationFilter` maps `AuthenticationException` → 401 and `AccessDeniedException` → 403.

> [!warning] Unverified traps from the dump
> - The HTTP name “Unauthorized” for 401 is identity, not permission. Saying “401 means not allowed” is the common mix-up.
> - A misconfigured filter that never sets `Authentication` often looks like 401 when the rule was meant to be a 403.
