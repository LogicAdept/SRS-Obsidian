<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

denyAll() blocks every request regardless of authentication. Dumps use it for maintenance or tests:

```
http.authorizeHttpRequests()
    .anyRequest().denyAll()
    .and().httpBasic();
```

Opposite of permitAll(). Expressions dumps also list denyAll as a SpEL access rule.
> [!warning] Unverified traps from the dump
> - denyAll on anyRequest after a permitAll public matcher is fine; denyAll first locks the whole app including login.
