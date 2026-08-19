<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JavaInUse dump: refresh token grant exchanges a refresh token for a new access token without the user’s password. Listed next to authorization code and client credentials. Resource servers still reject expired access tokens until the client presents a new one.
> [!warning] Unverified traps from the dump
> - Refreshing is typically the client + authorization server, not JwtDecoder on the resource server.
