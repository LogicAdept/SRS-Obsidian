<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**@Bean vs @Component?**

@Component (and stereotypes) on *your* class: component scan instantiates it. @Bean on a method in @Configuration: you construct the instance (third-party types, custom RestClient, DataSource). Don't put @Bean on a @Component class method and expect full configuration semantics — that's lite mode.
