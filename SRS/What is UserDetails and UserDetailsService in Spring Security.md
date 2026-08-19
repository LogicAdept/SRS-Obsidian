<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`UserDetails` is the user snapshot Spring Security authenticates against: username, hashed password, `GrantedAuthority` collection, and flags (`isEnabled`, `isAccountNonLocked`, `isAccountNonExpired`, `isCredentialsNonExpired`).

`UserDetailsService` loads that snapshot: `UserDetails loadUserByUsername(String username)` throws `UsernameNotFoundException`. Built-ins: `InMemoryUserDetailsManager`, `JdbcUserDetailsManager`, LDAP. Production usually implements it against your user table.

`DaoAuthenticationProvider` calls the service, then `PasswordEncoder.matches`. On success the `UserDetails` is stored as the `Authentication` principal.

> [!warning] Unverified traps from the dump
> - Returning `null` instead of throwing `UsernameNotFoundException` is a common bug.
> - Authorities must match how you check roles (`ROLE_` prefix vs `hasAuthority`).
