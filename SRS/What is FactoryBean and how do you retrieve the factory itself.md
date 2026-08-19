<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`FactoryBean` is a bean that **produces** another object. `getBean("name")` does not return the factory; it calls `getObject()` and returns that product (MyBatis `SqlSessionFactoryBean` → `SqlSessionFactory` is the usual example). Complex creation stays inside the factory instead of XML/`@Bean` soup.

To get the factory instance itself, prefix the name with `&` (`BeanFactory.FACTORY_BEAN_PREFIX`): `getBean("&name")`.

`isSingleton()` on the factory decides whether Spring caches the product. `false` means each `getBean` calls `getObject()` again.

The factory is still a managed bean (DI, lifecycle). Injection points that ask for the product type receive `getObject()`, not the factory.

> [!warning] Unverified traps from the dump
> - Forgetting `&` is why people say “I injected a FactoryBean and got the wrong type.”
> - Dumps claim “every bean has a FactoryBean”; that is a popular lie — only beans that implement the interface do.
