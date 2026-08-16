<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How does SecurityFilterChain work?**

Servlet filters before DispatcherServlet. SecurityFilterChain (Boot 3) is a bean built from HttpSecurity lambda DSL. Typical order: SecurityContext → CORS → CSRF → auth filters (UsernamePassword / BearerToken) → ExceptionTranslationFilter → AuthorizationFilter. Custom JWT: OncePerRequestFilter + addFilterBefore(..., UsernamePasswordAuthenticationFilter.class). Multiple chains with securityMatcher and @Order. Stateless API: SessionCreationPolicy.STATELESS.
