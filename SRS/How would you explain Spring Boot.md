<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Автоконфигурация Spring Boot.**

@EnableAutoConfiguration + @Conditional. Если DataSource в classpath — автоматически настроит JPA. Список: META-INF/spring/...AutoConfiguration.imports (Spring Boot 3+, раньше spring.factories).

**Spring vs Spring Boot?**

Framework: IoC, AOP, MVC, TX. Boot: auto-config, starters, embedded server, Actuator, opinionated jar. Still Spring underneath.
