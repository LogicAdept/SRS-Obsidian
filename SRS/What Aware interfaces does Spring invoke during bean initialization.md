<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

After instantiation and property injection, Spring calls **Aware** callbacks if the bean implements them, still **before** `@PostConstruct`:

- `BeanNameAware.setBeanName` — the id in the factory
- `BeanFactoryAware.setBeanFactory` — the owning factory
- `ApplicationContextAware.setApplicationContext` — the context (events, `getBean`, i18n)

They couple the class to Spring APIs. Prefer constructor injection of `ApplicationEventPublisher` / `Environment` when you can.

> [!warning] Unverified traps from the dump
> - Aware runs before init callbacks; using `getBean` for a not-yet-created collaborator can still fail.
> - `ApplicationContextAware` is a service-locator smell next to constructor injection.
