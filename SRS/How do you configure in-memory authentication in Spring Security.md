<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps store users in memory for demos and tests:

```java
auth.inMemoryAuthentication()
    .withUser("user").password("{noop}password").roles("USER")
    .and()
    .withUser("admin").password("{noop}password").roles("USER", "ADMIN");
```

Or an InMemoryUserDetailsManager / UserDetailsService bean with a PasswordEncoder. {noop} means no encoding; BCrypt is the dump production encoder.
> [!warning] Unverified traps from the dump
> - {noop} and withDefaultPasswordEncoder are not for production.
> - Defining a UserDetailsService bean turns off Boot’s default user; dumps that still expect the generated password then fail.
