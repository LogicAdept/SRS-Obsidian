<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`<context:annotation-config/>` registers four `BeanPostProcessor`s so annotation injection and lifecycle work without listing them by hand:

- `AutowiredAnnotationBeanPostProcessor` (`@Autowired` / `@Value`)
- `CommonAnnotationBeanPostProcessor` (`@Resource`, `@PostConstruct`, `@PreDestroy`)
- `PersistenceAnnotationBeanPostProcessor`
- `RequiredAnnotationBeanPostProcessor` (`@Required`)

`<context:component-scan>` implies the same processors (plus scanning). Java `AnnotationConfigApplicationContext` registers them as well.

> [!warning] Unverified traps from the dump
> - `annotation-config` does **not** scan for `@Component`; you still need `component-scan` or explicit bean definitions.
> - If you declare a custom `RequiredAnnotationBeanPostProcessor`, dumps say to disable the default annotation-config processors first.
