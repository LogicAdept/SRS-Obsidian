<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #SRS

# What happens if you replace `@Service` with `@Component` or `@Repository` on a service class?

> [!abstract] Short answer
> The class **stays a singleton bean** if it is still found by component scan: `@Service`, `@Component`, and `@Repository` are all **`@Component` stereotypes**. **`@Service` → `@Component`:** same registration and **no** extra interceptor today; you lose the **service-layer label** for tools and AOP pointcuts. The scanning chapter says **`@Service` is clearly the better choice** for that layer and may gain **more semantics later**. **`@Service` → `@Repository`:** still a bean, **plus** `@Repository` is already a marker for **persistence exception translation** (`PersistenceExceptionTranslationPostProcessor` → `DataAccessException`). That is the **DAO** stereotype, not a service. Full four-way map: [[What is the difference between Repository Component Controller and Service annotations]].

## Same scan, different extras

Classpath scanning treats `@Component` and every meta-annotation of it (`@Service`, `@Repository`, `@Controller`, `@Configuration`, …) as a candidate ([[How do you create a bean in Spring]]). Replacing the annotation does **not** drop the class from the context by itself. Default bean **name** still comes from the class (`invoiceService`) unless `value` / `@AliasFor` sets one.

```java
@Service
public class BillingService { /* ... */ }

@Component
public class BillingService { /* still scanned; no service pointcut */ }

@Repository
public class BillingService { /* scanned + exception-translation candidate */ }
```

**Listing 1.** Three stereotypes on the **same** service type. Only `@Repository` adds a documented **runtime** post-processor today.

```d2
Scan: "@ComponentScan"
Svc: "@Service\nlabel + future semantics"
Cmp: "@Component\ngeneric bean"
Repo: "@Repository\n+ PETPP proxy"
Scan -> Svc
Scan -> Cmp
Scan -> Repo
```

**Fig. 1.** All three register. `@Repository` is the one with **current extra behavior**.

**`@Component`:** generic “Spring-managed component.” Injection, `@Transactional`, and default scope behave as for `@Service`. Pointcuts written `within(@org.springframework.stereotype.Service *)` **miss** it. Tools that group “services” miss it too.

**`@Repository`:** persistence / DAO role. `PersistenceExceptionTranslationPostProcessor` (Boot: on by default via `spring.persistence.exceptiontranslation.enabled`) **proxies** `@Repository` beans ([[What is an AOP proxy in Spring]]) and maps store exceptions to Spring’s **`DataAccessException`** when a `PersistenceExceptionTranslator` is present (typical with JPA). On a **service** that is not a DAO, you get a misleading stereotype **and** an extra AOP wrapper you did not ask for.

`@Service` itself is `@Component` plus documentation (DDD “service” / façade). Spring does **not** currently add a service-layer interceptor — the dump’s “alias” is right for **runtime**, incomplete for **intent**.

> [!warning] `@Controller` is worse than either swap
> The cue is Component/Repository, but `@Controller` is **not** a synonym: `RequestMappingHandlerMapping` looks for **type-level `@Controller`**. Do not “try another stereotype” on a service that happens to have `@RequestMapping` methods.

> [!tip] Interview answer
> `@Component` instead of `@Service`: still a bean; worse for tools/aspects; docs tell you to keep `@Service` on the service layer. `@Repository` instead: still a bean **and** exception-translation proxy — that marker is for DAOs. Pick the stereotype that matches the layer, not whichever one “also scans.”
