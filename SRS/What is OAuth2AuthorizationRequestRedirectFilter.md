<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default order (~600): OAuth2AuthorizationRequestRedirectFilter redirects the browser to the IdP authorization endpoint (oauth2Login / login with Google/GitHub). It sits before UsernamePasswordAuthenticationFilter.
> [!warning] Unverified traps from the dump
> - This is the OAuth2 client/SSO redirect, not BearerTokenAuthenticationFilter on a resource server.
