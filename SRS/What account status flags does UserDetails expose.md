<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump UserDetails methods besides username/password/authorities:

- isAccountNonExpired
- isAccountNonLocked
- isCredentialsNonExpired
- isEnabled

DaoAuthenticationProvider rejects login using these flags without extra code. Custom UserDetails dumps often return true for all of them.
> [!warning] Unverified traps from the dump
> - A correct password still fails if isEnabled is false. That is not BadCredentials in every dump’s wording.
