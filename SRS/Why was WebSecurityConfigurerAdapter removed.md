<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What replaced WebSecurityConfigurerAdapter?**

Removed in Security 6. Configure a @Bean SecurityFilterChain securityFilterChain(HttpSecurity http). Component-based, multiple chains easier. Interview fail: extending the adapter on Boot 3.
