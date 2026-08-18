<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is @PreAuthorize / method security?**

AOP proxy (MethodSecurityInterceptor). EnableMethodSecurity (Boot 3; old @EnableGlobalMethodSecurity). SpEL on @PreAuthorize/@PostAuthorize, or @Secured. Same proxy limits: self-invocation, private/final. Boot 3: use EnableMethodSecurity; missing it is why @PreAuthorize 'stops working' after upgrade. Complements URL rules in SecurityFilterChain.
