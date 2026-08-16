<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Filter vs interceptor vs AOP?**

Filter: servlet API, before Spring MVC, CORS/security/gzip. Interceptor: inside DispatcherServlet, has HandlerMethod, pre/post handle. AOP: any Spring bean method (@Transactional, audit), not only web. Security belongs in the filter chain, not an MVC interceptor.
