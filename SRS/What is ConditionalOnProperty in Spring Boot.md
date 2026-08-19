<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is @ConditionalOnProperty?**

Источник: https://habr.com/ru/articles/967632/

Создаёт бин только если задано свойство в application.properties/yml. Пример: @ConditionalOnProperty(name = "app.payment.enabled", havingValue = "true").

**How do conditionals fit auto-config?**

Bean exists only if a property matches. Auto-config uses the same family (@ConditionalOnClass, OnMissingBean). Missing property → NoSuchBeanDefinitionException if something injects it.
