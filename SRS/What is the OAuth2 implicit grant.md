<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JavaInUse dump grant list: implicit grant returns a token in the browser redirect fragment (old SPA pattern). Alongside authorization code, password, client credentials, refresh.

Modern dumps prefer authorization code + PKCE for browser apps; implicit is the deprecated one.
> [!warning] Unverified traps from the dump
> - Spring Security 6 OAuth2 login samples are authorization-code, not implicit.
