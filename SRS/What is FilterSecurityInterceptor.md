<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps put FilterSecurityInterceptor late in the chain. It authorizes HTTP resources (URIs) and throws authentication/authorization exceptions when access is denied. ExceptionTranslationFilter sits above it and turns those exceptions into 401/403 or a login redirect.

It is a concrete AbstractSecurityInterceptor. Spring Security 6 dumps replace it with AuthorizationFilter / AuthorizationManager.
> [!warning] Unverified traps from the dump
> - If ExceptionTranslationFilter is missing, FilterSecurityInterceptor failures surface as 500 instead of 401/403.
