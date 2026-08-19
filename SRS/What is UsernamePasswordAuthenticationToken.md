<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: UsernamePasswordAuthenticationFilter extracts username and password and wraps them in UsernamePasswordAuthenticationToken (an Authentication). That unauthenticated token is what ProviderManager.authenticate receives.

The three-arg constructor (principal, credentials, authorities) is the authenticated form DaoAuthenticationProvider returns.
> [!warning] Unverified traps from the dump
> - Two-arg constructor is unauthenticated. Returning that from a custom AuthenticationProvider is not a successful login.
