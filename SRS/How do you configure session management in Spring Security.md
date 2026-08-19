<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps treat session management as SessionManagementFilter plus a SessionAuthenticationStrategy: timeouts, concurrent sessions, session fixation.

```java
http.sessionManagement()
    .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
    .maximumSessions(1)
    .maxSessionsPreventsLogin(true);
```

maximumSessions limits concurrent logins; maxSessionsPreventsLogin(true) rejects the new login instead of kicking the old session. JWT dumps set STATELESS.
> [!warning] Unverified traps from the dump
> - Concurrent session control needs a SessionRegistry; dumps that only set maximumSessions often omit that bean.
> - ALWAYS vs IF_REQUIRED vs NEVER vs STATELESS change whether a JSESSIONID is created at all.
