<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Implement AuthenticationProvider: authenticate() reads name/credentials, runs your logic, returns an authenticated UsernamePasswordAuthenticationToken (with authorities) or throws. supports() should accept only the token types you handle.

Dumps then auth.authenticationProvider(new CustomAuthenticationProvider()) on AuthenticationManagerBuilder (or expose the provider as a bean for the default ProviderManager).
> [!warning] Unverified traps from the dump
> - Returning an unauthenticated token is not success; set authorities and authenticated=true (the three-arg UsernamePasswordAuthenticationToken constructor).
> - An empty authorities list means later hasRole checks fail even after ‘login’.
