<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps split two handlers on exceptionHandling():

- AuthenticationEntryPoint — unauthenticated caller hits a protected resource (typically 401).
- AccessDeniedHandler — authenticated caller lacks permission (typically 403).

```java
http.exceptionHandling()
    .authenticationEntryPoint(new CustomAuthenticationEntryPoint())
    .accessDeniedHandler(new CustomAccessDeniedHandler());
```

ExceptionTranslationFilter sits in the chain and translates AuthenticationException / AccessDeniedException into those callbacks (or a login redirect for form login).
> [!warning] Unverified traps from the dump
> - 401 vs 403 is this split. Returning 401 for a logged-in user who lacks a role is the usual dump mistake.
> - For a JSON API, the default login redirect is wrong; you need an AuthenticationEntryPoint that writes 401 JSON.
