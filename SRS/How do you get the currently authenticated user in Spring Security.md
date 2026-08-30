<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps inject Principal, Authentication, or read SecurityContextHolder:

```java
String name = principal.getName();
Collection<? extends GrantedAuthority> roles = auth.getAuthorities();
```

Or Authentication auth = SecurityContextHolder.getContext().getAuthentication(). @AuthenticationPrincipal on a controller argument is the annotation form in later lists.
> [!warning] Unverified traps from the dump
> - Anonymous authentication still yields a non-null Authentication; check isAuthenticated() and the principal type.
> - Controller injection of Principal is request-thread only; @Async needs context propagation.
