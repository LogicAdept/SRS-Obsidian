<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list AuthorizationFilter as the filter that enforces access rules after authentication is set. It sits after ExceptionTranslationFilter in typical order lists.

It replaced FilterSecurityInterceptor / AccessDecisionManager in Spring Security 6 with AuthorizationManager. If this filter runs before an authentication filter, every request looks anonymous.
> [!warning] Unverified traps from the dump
> - Custom filters added after AuthorizationFilter are too late to set Authentication for that request.
