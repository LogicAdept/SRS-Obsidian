<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: AuthenticationEntryPoint is how unauthenticated requests are challenged — redirect to /login for form login, WWW-Authenticate for Basic, 401 JSON for APIs. ExceptionTranslationFilter invokes it on AuthenticationException (and anonymous AccessDeniedException).
> [!warning] Unverified traps from the dump
> - A REST API that still uses the default LoginUrlAuthenticationEntryPoint will 302 to HTML /login instead of 401.
