<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: InMemoryUserDetailsManager for tests/dev. JdbcUserDetailsManager when you will use the default users/authorities tables. Custom UserDetailsService (loadUserByUsername) for your own schema or user service. Pair any of them with a PasswordEncoder.
> [!warning] Unverified traps from the dump
> - {noop} and withDefaultPasswordEncoder in in-memory samples are not production encoders.
