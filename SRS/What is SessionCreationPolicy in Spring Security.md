<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SessionCreationPolicy is the dump’s switch for if Spring Security creates an HTTP session:

- IF_REQUIRED — default; create when needed.
- ALWAYS — create if needed (dump wording varies).
- NEVER — use an existing session, do not create.
- STATELESS — no session; SecurityContext is not written to HttpSession (JWT / API dumps).

Set via http.sessionManagement().sessionCreationPolicy(...).
> [!warning] Unverified traps from the dump
> - STATELESS does not by itself implement JWT; you still need a bearer filter or oauth2ResourceServer.
> - CSRF is session-oriented; dumps disable CSRF together with STATELESS for token APIs.
