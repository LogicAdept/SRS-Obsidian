<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Resource-server dumps: default clock-skew tolerance is about 60 seconds. If the authorization server’s clock is several minutes ahead, a ‘valid’ JWT looks expired and you get 401.

Fix: configure NimbusJwtDecoder with a larger clock skew. Confirm with TRACE logs that the failure is Token expired at ….
> [!warning] Unverified traps from the dump
> - Widening skew forever hides real expiry bugs. Dumps treat it as a staging/clock-sync issue first.
