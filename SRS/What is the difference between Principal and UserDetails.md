<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: java.security.Principal is getName() only (controller Principal parameter). UserDetails is Spring’s user: password hash, authorities, account flags. After login, Authentication.getPrincipal() is often a UserDetails, which is a Principal.
> [!warning] Unverified traps from the dump
> - Casting principal to UserDetails fails for JWT/OAuth2 dumps where principal is a Jwt or OidcUser.
