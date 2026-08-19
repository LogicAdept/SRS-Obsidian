<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps map Spring to well-known patterns:

- **Simple factory** — `BeanFactory.getBean(name)`
- **Factory method** — `FactoryBean.getObject()`
- **Singleton** — default bean scope (per container, not a JVM-wide GoF singleton)
- **Proxy** — AOP, `@Transactional`, scoped proxies
- **Template** — `JdbcTemplate` and similar boilerplate wrappers
- **Observer** — `ApplicationContext` events (`ApplicationListener`)
- **Front controller / MVC** — `DispatcherServlet`
- **Chain of responsibility** — Spring Security filter chain
- **Service locator** — `ServiceLocatorFactoryBean` / `getBean` lookups
- **Context object** — `ApplicationContext` as shared config
- **Adapter** — MVC `HandlerAdapter`

> [!warning] Unverified traps from the dump
> - Spring “singleton” is per `ApplicationContext`, not the classic GoF one-per-JVM singleton.
> - Not every bean is created through a user `FactoryBean`.
