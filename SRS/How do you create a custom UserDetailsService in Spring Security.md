<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Implement UserDetailsService and loadUserByUsername: look up the user, or throw UsernameNotFoundException. Return a UserDetails (Spring’s User or your own) with password, authorities, and account flags (locked / expired / disabled).

Register the bean; DaoAuthenticationProvider calls it during username/password login. Pair it with a PasswordEncoder so matches() hashes the presented password the same way as the stored hash.
> [!warning] Unverified traps from the dump
> - Returning null is not the contract; throw UsernameNotFoundException.
> - Account flags on UserDetails are why a correct password can still fail (locked, disabled, expired).
