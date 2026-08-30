<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default UserDetailsService in the form-login walkthrough: InMemoryUserDetailsManager (and auth.inMemoryAuthentication()). Users live in a map for tests and demos.

Production dumps replace it with JdbcUserDetailsManager or a custom UserDetailsService.
> [!warning] Unverified traps from the dump
> - A UserDetailsService @Bean turns off Boot’s generated user. Dumps that still expect the console password then fail.
