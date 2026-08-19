<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`BeanFactory` is the IoC **container** interface: it instantiates, configures, and wires beans and is the core of the factory that holds bean definitions. `ApplicationContext` is the usual advanced `BeanFactory`.

`FactoryBean` is a **bean that produces another object**. You implement it (or extend `AbstractFactoryBean`) when creation is too awkward for XML/`@Bean`. Dumps cite JNDI lookups (`JndiObjectFactoryBean`), classic AOP (`ProxyFactoryBean`), and Hibernate `LocalSessionFactoryBean`. `getBean("name")` returns `getObject()`, not the factory. Prefix `&` (`BeanFactory.FACTORY_BEAN_PREFIX`) to retrieve the factory itself.

> [!warning] Unverified traps from the dump
> - The names look like aliases; one is the container, the other is a special bean type.
> - Dumps claim you “rarely write custom FactoryBeans” because they are framework-specific and not useful outside the container.
