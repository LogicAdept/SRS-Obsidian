<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DependsOn` forces Spring to initialize named beans **before** this bean, even when there is no injected reference. Use it when initialization order matters for side effects (a bean that must run `@PostConstruct` before another starts).

Usual injection already orders beans; you do not need `@DependsOn` for a constructor/`@Autowired` dependency.

Class-level `@DependsOn` needs component scanning (or an equivalent `@Bean` method) or dumps say it has no effect.

> [!warning] Unverified traps from the dump
> - Missing named bean → `BeanCreationException` / `NoSuchBeanDefinitionException`.
> - Circular `@DependsOn` still fails. `@DependsOn` does not guarantee another bean’s `@PostConstruct` finished in every dump’s telling — verify against current docs at fill time.
