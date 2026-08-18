<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Spring Boot auto-configuration — как устроен?**

@EnableAutoConfiguration + @Conditional. Конфиги описаны в META- INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports (ранее — spring.factories).
