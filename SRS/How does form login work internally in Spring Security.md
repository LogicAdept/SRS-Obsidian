<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump walkthrough:

1. The browser POSTs credentials to the login-processing URL (/login by default).
2. UsernamePasswordAuthenticationFilter builds an unauthenticated Authentication and gives it to AuthenticationManager.
3. The manager delegates to an AuthenticationProvider (typically DaoAuthenticationProvider), which loads UserDetails and checks the password with PasswordEncoder.
4. On success a fully authenticated Authentication is stored in the SecurityContext. On failure an AuthenticationException is thrown and the user is sent back to the login page.

Naming AuthenticationManager → AuthenticationProvider → UserDetailsService in that order is the dump’s senior signal.
> [!warning] Unverified traps from the dump
> - This is session/cookie form login, not JWT. STATELESS APIs do not use this filter for each API call.
