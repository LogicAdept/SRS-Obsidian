<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump which-when: form login for a traditional app that owns usernames and passwords. OAuth2/OIDC login (oauth2Login) when you delegate identity to Google/GitHub/Keycloak and never handle the IdP password. HTTP Basic for simple machine clients.
> [!warning] Unverified traps from the dump
> - oauth2Login is the client/SSO path. oauth2ResourceServer is the API that validates bearer tokens. Mixing the two names is a common stumble.
