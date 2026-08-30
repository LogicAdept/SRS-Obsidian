<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: UserDetailsService only loadUserByUsername. UserDetailsManager extends it with createUser / updateUser / deleteUser / changePassword. InMemoryUserDetailsManager and JdbcUserDetailsManager are managers; a custom production service is often just UserDetailsService.
> [!warning] Unverified traps from the dump
> - DaoAuthenticationProvider only needs UserDetailsService. Extra manager methods are for admin CRUD, not login.
