<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Before, After, Around — what is the difference?**

@Before, @AfterReturning, @AfterThrowing, @After (finally), @Around. Around gets ProceedingJoinPoint.proceed() — can skip the method, change args/return, swallow exceptions. Join point in Spring AOP = method execution only. AspectJ is wider (fields, constructors) if you opt in.
