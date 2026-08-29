<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What is lite `@Bean` mode versus full `@Configuration` in Spring?

> [!abstract] Short answer
> **Full** mode: `@Bean` methods sit on a **`@Configuration`** class with **`proxyBeanMethods = true`** (the default since that flag arrived in **5.2**). Spring builds a **CGLIB subclass** so a Java call to another `@Bean` method is **intercepted** and returns the **container-managed** singleton (or other scope), not `new`. **Lite** mode: `@Bean` on a **non-`@Configuration`** type (`@Component`, a plain class) — or **`@Configuration(proxyBeanMethods = false)`**, which the `@Configuration` javadoc calls **behaviorally equivalent** to dropping `@Configuration`. Lite methods are **plain factories**: do **not** call other `@Bean` methods; use **parameters** / injection. No CGLIB → the class **may be `final`**. Usual advice: put `@Bean` methods on **full** `@Configuration` ([[What annotations are used to configure a Spring application context]]).

## CGLIB vs a factory method

Java-based container chapter: lite `@Bean` is a **bonus factory** on a type whose **primary** job is something else (for example a `@Service` exposing a management bean). Full `@Configuration` is a **source of bean definitions** whose **inter-bean** calls must go through the container so default **singleton** scope still holds ([[Which Spring configuration style do you prefer XML Java or annotations and why]]).

```java
@Configuration // full: proxyBeanMethods true
public class FullConfig {
	@Bean
	ClientDao clientDao() {
		return new ClientDaoImpl();
	}

	@Bean
	ClientService clientService() {
		return new ClientServiceImpl(clientDao()); // intercepted → one dao
	}
}

@Component // lite
public class LiteHost {
	@Bean
	ClientDao clientDao() {
		return new ClientDaoImpl();
	}

	@Bean
	ClientService clientService() {
		return new ClientServiceImpl(clientDao()); // raw Java → second dao
	}
}
```

**Listing 1.** Same `clientDao()` call. Full mode hits the singleton cache. Lite mode constructs **another** `ClientDaoImpl`. Fix lite with `ClientService clientService(ClientDao clientDao)`.

```d2
Full: "@Configuration\nCGLIB subclass"
Lite: "@Component + @Bean\nor proxyBeanMethods=false"
Full -> "clientDao() call": "container getBean"
Lite -> "clientDao() call": "plain invoke"
```

**Fig. 1.** Full mode **redirects** cross-method references. Lite does **not**.

`@Configuration` constraints (full / `proxyBeanMethods true`): supplied as a **class** (not a factory-produced instance), **non-final**, **non-local**, nested configs **`static`**. `@Bean` methods must not return further `@Configuration` types (those instances are ordinary beans; their config annotations are **ignored**). Nested `@Import` composition still works on full configs ([[How does Import register beans in Spring]]).

**`static @Bean`:** even on a full `@Configuration` class, **static** methods are **never** CGLIB-intercepted (cannot override `static`). Use `static` for `BeanFactoryPostProcessor` / `BeanPostProcessor` so the config class is not instantiated too early. Cross-calls to a static `@Bean` are **lite semantics**.

Boot auto-configuration often uses `@Configuration(proxyBeanMethods = false)` because each factory is **self-contained** and takes collaborators as **parameters**.

> [!warning] Lite is not “@Bean is illegal off @Configuration”
> The dump “must live on `@Configuration`” is the **interview trap**, not the rule. `@Bean` on `@Component` **is** supported. What **breaks** is treating `otherBean()` as a container lookup. `@Configuration(proxyBeanMethods = false)` looks like configuration and still **breaks** those calls the same way.

> [!tip] Interview answer
> Full `@Configuration`: CGLIB proxy, `otherBean()` is `getBean`. Lite (`@Bean` on `@Component`, or `proxyBeanMethods = false`): factory methods only — inject parameters, do not call sibling `@Bean` methods. Prefer full mode unless you opted out of the subclass on purpose.
