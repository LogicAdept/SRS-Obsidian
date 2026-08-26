<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between Spring `@Service`, `@Repository`, and `@Controller` annotations?

> [!abstract] Short answer
> All three are **`@Component` stereotypes** (scanned beans, default **singleton**). **`@Controller`** (2.5) is the **web** role: **`RequestMappingHandlerMapping.isHandler` requires type-level `@Controller`**. **`@RestController`** counts because it **is** `@Controller` + `@ResponseBody`. **`@Service`** (2.5) is a DDD / J2EE **business façade** label — Spring adds **no** service interceptor. **`@Repository`** (2.0) is a DDD **collection-like store** / DAO **and** the default pointcut for **`PersistenceExceptionTranslationPostProcessor`**: an **AOP proxy** maps native persistence exceptions to **`DataAccessException`**. **`@Transactional` is separate.**

## Same scan, three architectural roles

`@Component` javadoc: `@Service`, `@Controller`, and `@Repository` are stereotypes **meta-annotated with `@Component`**. `value` is the suggested bean name (custom stereotypes need **`@AliasFor Component.value`** as of Framework **6.1**). Four-way including generic `@Component`: [[What is the difference between Repository Component Controller and Service annotations]].

| Annotation | Role (javadoc) | Extra runtime |
| --- | --- | --- |
| `@Controller` | Web controller, usually with `@RequestMapping` | MVC **handler type**. `@GetMapping` on `@Service` is **not** mapped |
| `@Service` | Evans “standalone operation”; or Core J2EE **business façade** | **None.** Teams may narrow the meaning |
| `@Repository` | Evans repository / Jakarta **DAO** | Eligible for **`DataAccessException` translation** with **`PersistenceExceptionTranslationPostProcessor`** |

`RequestMappingHandlerMapping` (3.1+): **“Expects a handler to have a type-level `@Controller` annotation.”** PETPP: autodetects **`PersistenceExceptionTranslator`** beans (JPA `LocalContainerEntityManagerFactoryBean` implements it). Boot **4** registers that post-processor via **`PersistenceExceptionTranslationAutoConfiguration`** when the class is on the classpath. Translation is a **proxy**; **`this.method()`** inside the DAO skips it. Layering: [[What is the Spring MVC web layer]]. HTML vs JSON: [[What is the difference between Spring RestController and Controller]].

```java
@Controller
class AccountPageController {
    private final AccountService accounts;
    AccountPageController(AccountService accounts) { this.accounts = accounts; }

    @GetMapping("/accounts/{id}")
    String show(@PathVariable long id, Model model) {
        model.addAttribute("account", accounts.find(id));
        return "account";
    }
}

@Service
class AccountService {
    private final AccountRepository store;
    AccountService(AccountRepository store) { this.store = store; }
    Account find(long id) { return store.get(id); }
}

@Repository
class JpaAccountRepository implements AccountRepository {
    Account get(long id) { /* EntityManager; PersistenceException → DataAccessException */ }
}
```

**Listing 1.** Conceptual three-layer stereotypes. `@Controller` is the only one `HandlerMapping` cares about. `@Service` is orchestration. `@Repository` is storage + optional translation.

```d2
direction: down
c: "@Controller\nHTTP handler" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
s: "@Service\nfaçade, no extra AOP" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
r: "@Repository\n+ DataAccessException proxy" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

c -> s -> r
```

**Fig. 1.** Typical call chain. Mixing the annotations does not move the extra behavior: MVC mapping stays on `@Controller`; translation stays on `@Repository`.

> [!warning] `@GetMapping` on `@Service` never becomes an endpoint
> The class is still a bean. **`isHandler` is false.** Result: **404**, not a startup mapping error.

> [!warning] `@Repository` is not `@Transactional`
> Exception translation does **not** start a transaction. A `@Service` with `@Repository` on it can get a persistence-exception **proxy** you did not want, still **without** a transaction.

> [!warning] `@Controller` does not translate JDBC/JPA exceptions
> Uncaught `SQLException` / `PersistenceException` bubble as servlet errors unless a **`@ExceptionHandler`** or translation on the **repository** (or a translator on that bean) maps them.

> [!tip] Interview answer
> **`@Controller` is what Spring MVC maps; `@Service` is a scanned façade with no extra interceptor; `@Repository` is the DAO stereotype plus `DataAccessException` translation when PETPP is present.** They are all `@Component`. Do not put `@GetMapping` on a service and expect a URL.
