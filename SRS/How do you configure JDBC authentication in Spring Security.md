<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps use jdbcAuthentication() on AuthenticationManagerBuilder with a DataSource and optional SQL:

```java
auth.jdbcAuthentication().dataSource(dataSource)
    .usersByUsernameQuery("select username, password, enabled from users where username=?")
    .authoritiesByUsernameQuery("select username, authority from authorities where username=?");
```

Default schema expects users(username, password, enabled) and authorities(username, authority). Passwords must already be encoded for the configured PasswordEncoder.
> [!warning] Unverified traps from the dump
> - Plain-text passwords in those tables fail once BCrypt is on.
> - This is Spring Security JDBC auth, not Spring Data JPA. A custom UserDetailsService over JPA is the usual replacement.
