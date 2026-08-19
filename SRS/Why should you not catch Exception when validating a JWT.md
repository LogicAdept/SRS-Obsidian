<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump anti-pattern: parseClaimsJws in try/catch Exception return false. That swallows ExpiredJwtException, MalformedJwtException, SignatureException, UnsupportedJwtException.

Expired is normal. Invalid signature may be tampering. Dumps say catch them separately and log the specific reason for monitoring.
> [!warning] Unverified traps from the dump
> - Returning false for every failure also hides configuration bugs (wrong key, wrong parser).
