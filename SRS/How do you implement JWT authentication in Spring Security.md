<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #Security/OAuth2 #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How do you do JWT in Spring Boot?**

Two paths: (1) Resource server starter — issuer-uri, JWKS, oauth2ResourceServer().jwt() — don't write a parser. (2) Custom login that issues JWT + OncePerRequestFilter that validates, builds UsernamePasswordAuthenticationToken, SecurityContextHolder. Stateless, CSRF off for bearer APIs. Cannot revoke a JWT without a blocklist or short TTL+refresh.
