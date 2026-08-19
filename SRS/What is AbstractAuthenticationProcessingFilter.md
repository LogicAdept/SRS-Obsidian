<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump architecture: AbstractAuthenticationProcessingFilter is the base servlet filter for submitting credentials. UsernamePasswordAuthenticationFilter is the usual subclass: build an Authentication from the request, call AuthenticationManager, then success/failure handlers and RememberMeServices.
> [!warning] Unverified traps from the dump
> - BearerTokenAuthenticationFilter is not this hierarchy in Security 6 dumps — it is the OAuth2 resource-server filter, not form-login’s abstract parent.
