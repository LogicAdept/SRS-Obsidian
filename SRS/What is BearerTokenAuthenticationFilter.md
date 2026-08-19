<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps name BearerTokenAuthenticationFilter as the filter that reads Authorization: Bearer … for OAuth2 resource servers / JWT, then the Authentication is available for AuthorizationFilter.

Custom JWT samples often roll OncePerRequestFilter instead of this built-in. Order: authentication filters before ExceptionTranslationFilter and AuthorizationFilter.
> [!warning] Unverified traps from the dump
> - If this filter never runs (wrong SecurityFilterChain matcher), controllers see anonymous even with a Bearer header.
