<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Two dump recipes:

1. permitAll on those paths in HttpSecurity (still runs the security filter chain):
```java
http.authorizeRequests()
    .antMatchers("/public/**", "/actuator/**").permitAll()
    .anyRequest().authenticated();
```

2. Drop them out of the chain entirely (old WebSecurity.ignoring, later WebSecurityCustomizer):
```java
web.ignoring().antMatchers("/css/**", "/js/**");
```
> [!warning] Unverified traps from the dump
> - ignoring() skips CSRF, security headers, and logging. Prefer permitAll unless you truly need the filters gone.
> - Actuator dumps that permitAll /actuator/** accidentally expose health and env.
