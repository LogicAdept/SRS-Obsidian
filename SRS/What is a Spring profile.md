<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #DevOps/Configuration #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Profiles helps to segregating application configurations, and make them available only in certain environments. Any `@Component` or `@Configuration` can be marked with `@Profile` to limit when it is loaded. You can define default configuration in application.properties. Environment specific overrides can be configured in specific files:

* application-dev.properties
* application-qa.properties
* application-stage.properties
* application-prod.properties

**Using Profiles In Code**
```java
@Configuration
@Profile("dev")
public class DevConfigurations {
    // DEV Configurations
}
@Configuration
@Profile("prod")
public class ProdConfigurations {
    // Production Configurations
}
```

**What does @Profile do?**

Источник: https://habr.com/ru/articles/967632/

Условное включение бина/конфигурации по активному профилю. Если бин с @Profile внедряют при неактивном профиле — NoSuchBeanDefinitionException.
