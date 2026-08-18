<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How does AuthenticationProvider chain work?**

AuthenticationManager (usually ProviderManager) iterates AuthenticationProviders; first non-null success wins; order matters. DaoAuthenticationProvider for passwords, JwtAuthenticationProvider for resource server. Wrong order → JWT sent to LDAP/password provider → 401. Use @Order or explicit list. supports() + authenticate().
