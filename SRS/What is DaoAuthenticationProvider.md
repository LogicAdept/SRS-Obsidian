<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

DaoAuthenticationProvider is the username/password AuthenticationProvider. It calls UserDetailsService.loadUserByUsername, then PasswordEncoder.matches, then account-status flags (locked, disabled, expired).

It is the default for form login and HTTP Basic. Custom providers or JWT/OAuth2 providers must be ordered so they are not shadowed by this one — dumps put JWT/LDAP vs DAO order as a 401 source.
> [!warning] Unverified traps from the dump
> - hideUserNotFoundExceptions turns UsernameNotFoundException into BadCredentialsException so user enumeration is harder.
