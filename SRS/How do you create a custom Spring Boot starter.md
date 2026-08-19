<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How do you write a custom starter?**

Module with autoconfigure: @AutoConfiguration class + @Conditional* + AutoConfiguration.imports. Optional spring-boot-starter-* pom that depends on it. Don't scan the library with the app's @ComponentScan; register via auto-config. Expose ConfigurationProperties with a prefix. Document what OnMissingBean the user can override.
