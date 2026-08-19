<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Why must @Bean methods live on @Configuration?**

Full @Configuration is CGLIB-proxied: calling another @Bean method returns the container singleton. On a plain @Component (lite), b() inside a() is a raw Java call → new instance, breaks singleton. Interview trap.
