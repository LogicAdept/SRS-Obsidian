<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Why prefer constructor injection over field injection?**

Required deps can be final, object is fully initialized, easy to unit-test without Spring, cycles fail fast. Field @Autowired hides deps, needs reflection/container in tests, allows partially constructed objects. Since Spring 4.3 a single constructor does not need @Autowired. Use setter only for optional deps.
