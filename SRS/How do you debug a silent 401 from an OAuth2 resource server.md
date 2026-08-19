<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the HTTP body is deliberately vague. Enable TRACE logging for org.springframework.security.oauth2. Then you see expired, wrong issuer, bad signature, or clock skew.

Also check: JwtDecoder bean present, JWK set URI reachable, CSRF on POST (403/401 confusion), CORS on browser calls.
> [!warning] Unverified traps from the dump
> - Do not leave TRACE on in production except while debugging.
