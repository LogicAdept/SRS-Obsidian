<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Security 6 dump recipe: a SecurityFilterChain @Bean, lambda DSL, requestMatchers, finish with anyRequest():

```
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/public/**").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated());
return http.build();
```

authorizeHttpRequests replaced authorizeRequests; requestMatchers replaced antMatchers/mvcMatchers.
> [!warning] Unverified traps from the dump
> - Leaving out anyRequest() can leave paths unsecured.
