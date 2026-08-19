<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If several init callbacks are present, dumps give this order after `BeanPostProcessor.postProcessBeforeInitialization`:

1. `@PostConstruct`
2. `InitializingBean.afterPropertiesSet()`
3. custom `init-method` / `@Bean(initMethod)`

Then `BeanPostProcessor.postProcessAfterInitialization` (AOP proxies are created here in dump wording). Destroy is the mirror: `@PreDestroy` → `DisposableBean.destroy()` → `destroy-method`.

> [!warning] Unverified traps from the dump
> - Init methods run on the **original** instance, before the after-init processors wrap it in a proxy. Calling `@Transactional` from `@PostConstruct` is a common miss.
> - Dumps disagree on whether `CommonAnnotationBeanPostProcessor` fires `@PostConstruct` inside “before init” or as a separate step; verify at fill time.
