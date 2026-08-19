<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

On an OAuth2 resource server, JwtDecoder decodes and validates a bearer JWT (signature via JWK set, exp, issuer, audience). Spring Boot auto-configures it from spring.security.oauth2.resourceserver.jwt.issuer-uri (Nimbus).

If the bean is missing, dumps say Spring may fall back to opaque-token introspection. If the authorization server has no introspection endpoint, you get a 401. Failures become JwtException; the filter maps that to 401 without leaking the reason in the body.
> [!warning] Unverified traps from the dump
> - Missing spring-security-oauth2-jose / resource-server starter is a common ‘no JwtDecoder’ cause.
