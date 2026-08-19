<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Opaque access tokens are not self-contained JWTs. The resource server asks the authorization server’s introspection endpoint whether the token is active.

Dumps: if JwtDecoder is missing, Spring Security may try opaque introspection instead. If the server has no introspection, every call is 401. JWT resource servers should not fall through to this accidentally.
> [!warning] Unverified traps from the dump
> - Introspection is a network hop per request; JWT dumps prefer local JWK validation for that reason.
