<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump sibling of AuthenticationSuccessHandler: runs when AuthenticationException is thrown on form login (bad password, locked). Default redirects back to /login?error. REST dumps write 401 JSON instead of a redirect.
> [!warning] Unverified traps from the dump
> - It is not AccessDeniedHandler (403 after you are already authenticated).
