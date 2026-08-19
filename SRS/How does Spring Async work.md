<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Async #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How does @Async work?**

Proxy submits the method to a TaskExecutor, returns immediately (void or Future/CompletableFuture). EnableAsync. Default executor is simple and not for production — define ThreadPoolTaskExecutor. Self-invocation skips @Async. Exceptions on void @Async go to AsyncUncaughtExceptionHandler. Same limits as other AOP: public method, not final.
