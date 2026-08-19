<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list: HTTP Basic, form login, digest, LDAP, OAuth2, JWT (bearer), OpenID Connect, plus in-memory and JDBC/DAO username-password. Remember-me, anonymous, X.509, and SAML appear in older lists.

They all produce an Authentication in the SecurityContext; the filter (form, Basic, Bearer, oauth2Login, …) is what differs.
> [!warning] Unverified traps from the dump
> - OAuth2 password grant and implicit grant show up in dumps; both are obsolete in current OAuth2 practice.
> - JWT is not a separate Spring ‘mode’ by itself: it is usually oauth2ResourceServer().jwt() or a custom Bearer filter.
