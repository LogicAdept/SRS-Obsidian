<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Batch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: add spring-boot-starter-batch and starter-security, then protect job endpoints:

```
http.authorizeRequests()
    .antMatchers("/batch/**").authenticated()
    .anyRequest().permitAll()
    .and().httpBasic();
```

Only authenticated callers start/stop/view jobs. The job @Bean itself is not a substitute for HTTP security on the actuator/launch API.
> [!warning] Unverified traps from the dump
> - Securing /batch/** does not authenticate a CommandLineRunner job that starts inside the same JVM with no HTTP call.
