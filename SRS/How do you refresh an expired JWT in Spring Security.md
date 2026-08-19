<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: if access JWT expiry throws JWTExpiredException, the client calls a second API with the expired (or refresh) token and receives a new access JWT.

That is application/token-endpoint behavior, not a built-in PasswordEncoder feature. Resource servers still reject expired access tokens until the client presents a new one.
> [!warning] Unverified traps from the dump
> - Accepting an expired access token on every API call without a dedicated refresh step is the dump’s anti-pattern.
