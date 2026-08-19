<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: an OAuth2 client delegates login to an authorization server and receives identity/tokens. A resource server is an API that validates an incoming bearer token on each request (often JWT via oauth2ResourceServer().jwt()).

JWT is the usual token format for the resource-server side — self-contained signature and claims, no introspection round-trip in the dump happy path.
> [!warning] Unverified traps from the dump
> - @EnableOAuth2Sso / @EnableResourceServer are the deprecated Boot/OAuth2 pairing, not Security 6’s oauth2Login + oauth2ResourceServer.
