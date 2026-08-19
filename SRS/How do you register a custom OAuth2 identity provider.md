<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: spring.security.oauth2.client.registration plus a matching provider (authorization-uri, token-uri, user-info-uri), grant authorization_code, then oauth2Login().

That is a generic IdP (not only Google/GitHub CommonOAuth2Provider). client-id, client-secret, redirect-uri {baseUrl}/login/oauth2/code/{registrationId}, scopes profile/email in the sample.
> [!warning] Unverified traps from the dump
> - redirect-uri must match the IdP registration exactly, including the /login/oauth2/code/{id} path.
