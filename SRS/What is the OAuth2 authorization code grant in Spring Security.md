<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Authorization code is the browser grant: the app opens the authorization server, the user consents, the app receives a code on the redirect, then exchanges code+client secret (or PKCE) for an access token.

Spring Security dumps map this to oauth2Login() (client) with registration and provider URIs in application.yml. It is the grant for ‘Login with Google’, not for machine-to-machine.
> [!warning] Unverified traps from the dump
> - Never send the access token in the first redirect; the code is the one-time ticket.
> - Public clients should use PKCE; dumps that only show client-secret in a SPA are dated.
