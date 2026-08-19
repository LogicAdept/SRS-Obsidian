<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

authorizeHttpRequests / authorizeRequests rules are evaluated in declaration order; the first match wins.

Put specific patterns before broad ones:

```
.requestMatchers("/admin/**").hasRole("ADMIN")
.anyRequest().authenticated()
```

If you reverse those, /** or anyRequest() matches /admin/** first and the admin rule never runs. Dumps call this shadowing.
> [!warning] Unverified traps from the dump
> - anyRequest().authenticated() first makes later permitAll unreachable.
