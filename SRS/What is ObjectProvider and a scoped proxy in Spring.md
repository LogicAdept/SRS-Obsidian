<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How do you get a new prototype from a singleton?**

Injecting prototype into singleton captures one instance. Fixes: ObjectProvider.getObject() each call, @Lookup method injection, scoped proxy (@Scope(proxyMode=TARGET_CLASS)). Interview follow-up to the prototype-in-singleton gotcha.
