<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ProviderManager is the default AuthenticationManager. It does not authenticate itself; it iterates AuthenticationProvider instances.

Each authenticate() may: return an authenticated Authentication; throw AuthenticationException (bad credentials); or return null (cannot decide). Dumps say a parent AuthenticationManager is tried if all providers return null.
> [!warning] Unverified traps from the dump
> - ProviderNotFoundException means no provider supported the Authentication type — often a custom token you forgot to supports().
> - hideUserNotFoundExceptions on DaoAuthenticationProvider turns UsernameNotFoundException into BadCredentialsException on purpose.
