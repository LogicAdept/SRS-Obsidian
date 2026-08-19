<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps give two remember-me techniques:

- Hash-based cookie tokens (signature over username/expiry/password/key). No extra table; stealing the cookie plus a password change story varies by version.
- Persistent tokens stored in a database (series/token). The cookie is a pointer; a stolen token can be revoked by deleting the row.

RememberMeAuthenticationFilter consumes the cookie on later visits so the user skips the login form.
> [!warning] Unverified traps from the dump
> - A guessable remember-me key forges hash tokens. Persistent tokens need a token repository bean, not only rememberMe().key(...).
