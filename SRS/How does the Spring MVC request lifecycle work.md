<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Walk through an HTTP request in Spring MVC.**

Filter chain (Security) → DispatcherServlet → HandlerMapping finds @RequestMapping → interceptors preHandle → HandlerAdapter invokes controller (argument resolvers: @PathVariable, @RequestBody) → return value handlers / HttpMessageConverter → interceptors postHandle/afterCompletion → response. Exceptions: HandlerExceptionResolver / @ControllerAdvice.
