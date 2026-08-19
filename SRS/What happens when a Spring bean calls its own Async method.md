<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Async #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**@Async self-invocation?**

Same proxy issue as @Transactional: this.async() runs synchronously on the caller thread. Call via injected proxy or another bean. Need @EnableAsync and a real executor.
