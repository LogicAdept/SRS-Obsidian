<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump logout code: SecurityContextLogoutHandler.logout(request, response, auth) clears the SecurityContext and invalidates the session for a programmatic logout (controller calling logout instead of only POST /logout).

http.logout() uses handlers like this under the hood.
> [!warning] Unverified traps from the dump
> - Clearing the context without invalidating the session can leave a JSESSIONID that still looks logged in on the next request if something reloads the old context.
