<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Password (resource-owner) grant: the user gives username and password to the client; the client sends those plus client-id/secret to the token endpoint and gets an access token.

Dump example: a native/mobile app logging into Facebook with the user’s password. Spring Boot samples historically used this grant. It is not authorization-code (browser redirect) and not client-credentials (no user).
> [!warning] Unverified traps from the dump
> - OAuth 2.1 and current providers deprecate the password grant. Interviews that still ask it want the flow, then the ‘do not use it’ follow-up.
