<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say the default login URL is /login. An unauthenticated request to a protected resource is redirected there (form login) or challenged with 401 (HTTP Basic / JWT).

The generated default login page is served when you call formLogin() without loginPage(...).
> [!warning] Unverified traps from the dump
> - Changing loginPage does not always change the processing URL; dumps often forget loginProcessingUrl.
