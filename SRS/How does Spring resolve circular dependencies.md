<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is a circular dependency and how does Spring handle it?**

A needs B, B needs A. Setter/field injection: Spring can expose an early singleton reference and finish injecting later. Constructor injection of two singletons: fails at startup (BeanCurrentlyInCreationException) — this is preferred because the cycle is visible. Fixes: break the cycle (extract third bean), @Lazy on one constructor arg, setter for the optional side. Don't 'fix' with field injection just to hide the cycle.
