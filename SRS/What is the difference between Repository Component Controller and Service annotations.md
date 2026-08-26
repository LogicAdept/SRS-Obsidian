<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `@Repository`, `@Component`, `@Controller`, and `@Service`?

> [!abstract] Short answer
> They are all **`@Component` stereotypes** for **classpath scanning**. **`@Component`** is the generic marker. **`@Service`** is a DDD / “business façade” label with **no extra runtime interceptor**. **`@Repository`** is a DDD persistence role **and** the pointcut for **`PersistenceExceptionTranslationPostProcessor`**, which proxies the bean and maps store exceptions to **`DataAccessException`**. **`@Controller`** is the web stereotype: **`RequestMappingHandlerMapping` only treats type-level `@Controller` as a handler**. **`@RestController`** is `@Controller` + `@ResponseBody`. Default scope for all of them is **singleton**.

## Same scan, different extras

`@Component` javadoc: any meta-annotation of `@Component` is a stereotype (`@Service`, `@Controller`, `@Repository`). `value` becomes the bean name. Custom stereotypes must **`@AliasFor` `Component.value`** (Framework 6.1+).

`@Service` javadoc: Evans DDD “service” / J2EE business façade. Teams may narrow the meaning; Spring does **not** add a service interceptor.

`@Repository` javadoc: Evans “collection-like storage”. With `PersistenceExceptionTranslationPostProcessor` (Boot: **`spring.dao.exceptiontranslation.enabled`**, default **true**), native persistence exceptions become Spring’s **`DataAccessException`**. Needs a **`PersistenceExceptionTranslator`** on the context (JPA `EntityManagerFactory` beans already implement it). Translation is an **AOP proxy**.

`@Controller` javadoc: web controller, typically with `@RequestMapping` methods. `RequestMappingHandlerMapping.isHandler` **requires type-level `@Controller`**. A `@Service` with `@GetMapping` methods is a bean, **not** a mapped controller. `@RestController` (since 4.0) composes `@Controller` + `@ResponseBody`.

```java
@Component
class ClockHolder { }

@Service
class BillingService { }

@Repository
class JpaOrderRepository { }   // exception translation if PETPP is registered

@Controller
class PageController {
    @GetMapping("/home")
    String home() { return "home"; }   // view name
}

@RestController
class OrderApi {
    @GetMapping("/orders/{id}")
    Order get(@PathVariable long id) { /* body */ }
}
```

**Listing 1.** Conceptual stereotypes. HTML vs JSON: [[What is the difference between Spring RestController and Controller]]. Creating MVC types: [[How do you create a Spring MVC controller]]. Scope: [[What is the default scope of a Spring MVC controller]].

```d2
direction: down
comp: "@Component\nscan candidate" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
svc: "@Service\nrole only" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
repo: "@Repository\n+ DataAccessException proxy" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ctrl: "@Controller\nHandlerMapping" {
  width: 240
  height: 45
  style.fill: "#fce4ec"
}
rest: "@RestController\nController + ResponseBody" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}

comp -> svc
comp -> repo
comp -> ctrl
ctrl -> rest
```

**Fig. 1.** Scan is shared. Only `@Repository` and `@Controller` / `@RestController` change runtime web or persistence behavior.

> [!warning] `@GetMapping` on `@Service` is invisible
> `RequestMappingHandlerMapping` looks for **`@Controller`**. Stereotype mix-ups produce a bean that never handles HTTP.

> [!warning] `@Repository` on a service does not “add transactions”
> Exception translation is **not** `@Transactional`. Putting `@Repository` on a non-DAO class can wrap it in a persistence-exception proxy you did not intend.

> [!warning] Self-invocation skips translation
> `this.save()` inside a `@Repository` does not go through the advisor. Same proxy rule as other Spring AOP.

> [!tip] Interview answer
> **`@Component` is the scan marker; the others are specializations.** `@Service` is documentation. `@Repository` enables **`DataAccessException` translation**. `@Controller` is what MVC actually maps; `@RestController` writes the body instead of a view name.
