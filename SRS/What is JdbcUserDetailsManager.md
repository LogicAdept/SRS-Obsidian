<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump built-in UserDetailsService for a relational store: JdbcUserDetailsManager (alongside InMemoryUserDetailsManager and LDAP). jdbcAuthentication().dataSource(...) wires the same idea.

Default tables: users(username, password, enabled) and authorities(username, authority). Passwords must match the PasswordEncoder.
> [!warning] Unverified traps from the dump
> - This is not Spring Data JPA. A custom UserDetailsService over JPA is the usual replacement.
