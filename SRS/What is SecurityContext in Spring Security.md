<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SecurityContext holds authentication and request-specific security data for the current execution. It stores the Authentication (the principal): username, credentials, authorities, and whether the user is authenticated.

To read the current user you obtain the SecurityContext first (usually via SecurityContextHolder), then getAuthentication().
> [!warning] Unverified traps from the dump
> - SecurityContext is the store; SecurityContextHolder is the accessor. Mixing the two names is a common dump mix-up.
> - Default storage is ThreadLocal, so handing work to another thread drops the context unless you propagate it.
