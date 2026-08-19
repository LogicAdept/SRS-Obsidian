<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps use authorizeRequests plus hasRole on path patterns:

```java
http.authorizeRequests()
    .antMatchers("/admin/**").hasRole("ADMIN")
    .antMatchers("/user/**").hasRole("USER")
    .anyRequest().authenticated();
```

The same idea in Security 6 is authorizeHttpRequests and requestMatchers. Method-level @PreAuthorize("hasRole('ADMIN')") is the other dump recipe (RBAC).
> [!warning] Unverified traps from the dump
> - hasRole("ADMIN") looks for ROLE_ADMIN. hasAuthority("ADMIN") does not add that prefix.
> - More specific matchers must be declared before anyRequest(); order matters.
