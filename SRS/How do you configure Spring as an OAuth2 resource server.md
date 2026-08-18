<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**OAuth2 client vs resource server?**

Client: obtains tokens (authorization code + PKCE) to call others. Resource server: validates incoming JWTs (signature, iss, exp, audience). starter oauth2-resource-server + spring.security.oauth2.resourceserver.jwt.issuer-uri. OIDC is auth on top of OAuth2. Don't confuse Keycloak-as-issuer with a homemade filter.
