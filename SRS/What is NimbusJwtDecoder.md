<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: resource-server JWT validation uses the Nimbus JOSE library. NimbusJwtDecoder verifies signature against the JWK set, expiry (with clock skew), issuer, and audience. Failure → JwtException → 401, reason only in TRACE logs.

Auto-configured when issuer-uri or jwk-set-uri is set.
> [!warning] Unverified traps from the dump
> - A custom JwtDecoder bean replaces auto-config; a broken bean looks like ‘Spring Security is not validating JWTs’.
