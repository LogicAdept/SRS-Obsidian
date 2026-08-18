<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How does auto-configuration work internally?**

Starters put AutoConfiguration classes on the classpath. Boot 2.7+/3: META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports (spring.factories is legacy). Each class is @ConditionalOnClass / OnMissingBean / OnProperty / OnWebApplication. User @Bean wins over auto-config if OnMissingBean. Debug: --debug or ConditionEvaluationReport in Actuator.
