<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `@Repository`, `@Component`, `@Controller`, and `@Service`?

> [!abstract] Short answer
> They are all **`@Component` stereotypes** for **classpath scanning** — the usual answer to “which stereotypes exist besides `@Service`.” **`@Component`** is the generic marker. **`@Service`** is a DDD / “business façade” label with **no extra runtime interceptor**. **`@Repository`** is a DDD persistence role **and** the pointcut for **`PersistenceExceptionTranslationPostProcessor`**, which proxies the bean and maps store exceptions to **`DataAccessException`**. **`@Controller`** is the web stereotype: **`RequestMappingHandlerMapping` only treats type-level `@Controller` as a handler**. **`@RestController`** is `@Controller` + `@ResponseBody`. **`@Configuration`** is a definition factory (still a `@Component`). Default scope for all of them is **singleton**. **`@Bean` is a method, not a stereotype.**

## Same scan, different extras

`@Component` javadoc: any meta-annotation of `@Component` is a stereotype (`@Service`, `@Controller`, `@Repository`). `value` becomes the bean name. Custom stereotypes must **`@AliasFor` `Component.value`** (Framework 6.1+). **`@Repository`** dates to **2.0**; **`@Service`** and **`@Controller`** to **2.5**.

`@Service` javadoc: Evans DDD “service” / J2EE business façade. Teams may narrow the meaning; Spring does **not** add a service interceptor.

`@Repository` javadoc: Evans “collection-like storage”. With `PersistenceExceptionTranslationPostProcessor` (Boot: **`PersistenceExceptionTranslationAutoConfiguration`**, property **`spring.dao.exceptiontranslation.enabled`**, default **true**), native persistence exceptions become Spring’s **`DataAccessException`**. Needs a **`PersistenceExceptionTranslator`** on the context (JPA `EntityManagerFactory` beans already implement it). Translation is an **AOP proxy**.

`@Controller` javadoc: web controller, typically with `@RequestMapping` methods. `RequestMappingHandlerMapping` (3.1+) **`isHandler` requires type-level `@Controller`**. A `@Service` with `@GetMapping` methods is a bean, **not** a mapped controller. `@RestController` (since 4.0) composes `@Controller` + `@ResponseBody`. `@ControllerAdvice` / `@RestControllerAdvice` are likewise `@Component` specializations for **global** web advice. Web layer split: [[What is the Spring MVC web layer]].

You may **compose your own** `@Component` meta-annotation. Default scan filters also pick **`@Named` / `@ManagedBean`**, which are **not** composable Spring stereotypes — build custom roles on **`@Component`**. **`@Bean` creates some other object from a method**; it does not mark “this class is a scanned component.” Without a scan (or `@Import` / `register`) all of these annotations are **inert**.

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

> [!warning] `@Controller` does not translate JDBC/JPA exceptions
> Uncaught `SQLException` / `PersistenceException` bubble as servlet errors unless a **`@ExceptionHandler`** or translation on the **repository** maps them.

> [!warning] `@Bean` and `@Autowired` are not stereotypes
> `@Bean` **creates some other object** from a method. `@Autowired` **injects**. Neither marks “this class is a scanned component.” JSR-330 `@Named` can be **detected** like `@Component`, but it is **not composable**.

> [!tip] Interview answer
> **`@Component` is the scan marker; the others are specializations.** Besides `@Service`: `@Component`, `@Repository`, `@Controller`, `@RestController`, `@Configuration`, plus any `@Component` meta-annotation you write. `@Service` is documentation. `@Repository` enables **`DataAccessException` translation**. `@Controller` is what MVC actually maps; `@RestController` writes the body instead of a view name. `@Bean` is not in that list.
