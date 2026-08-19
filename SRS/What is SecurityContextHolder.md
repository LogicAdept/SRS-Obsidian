<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`SecurityContextHolder` is the static holder for the current `SecurityContext`. The context holds the `Authentication` (principal, credentials, authorities).

Default strategy is `ThreadLocal`, so the authenticated user is visible downstream on the same thread. A custom filter typically does `SecurityContextHolder.getContext().setAuthentication(auth)`.

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
String username = auth.getName();
```

> [!warning] Unverified traps from the dump
> - Handing work to another thread drops the context unless you propagate it (`DelegatingSecurityContextRunnable`, MODE_INHERITABLETHREADLOCAL, or explicit copy).
> - Clearing the context at the end of the request matters for thread pools.
