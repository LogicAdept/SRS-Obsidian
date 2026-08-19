<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @EnableWebSecurity turns on the servlet filter chain (SecurityFilterChain / HttpSecurity). @EnableMethodSecurity turns on AOP method annotations. One does not enable the other.

URL rules do not protect a @Scheduled job or a message listener; method security does.
> [!warning] Unverified traps from the dump
> - Boot 3: @EnableWebSecurity plus leftover @EnableGlobalMethodSecurity is not @EnableMethodSecurity.
