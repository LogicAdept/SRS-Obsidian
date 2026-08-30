<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

UserDetailsService.loadUserByUsername must throw UsernameNotFoundException when the user is missing — dumps say do not return null.

DaoAuthenticationProvider can hide that exception as BadCredentialsException (hideUserNotFoundExceptions) so callers cannot tell unknown user from wrong password.
> [!warning] Unverified traps from the dump
> - Returning null is not the contract and can NPE inside the provider.
