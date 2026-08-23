<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #Java/Annotations #SRS

# Where is the `Transactional` annotation used in Spring?

> [!abstract] Short answer
> On **Spring-managed beans** in the same **`ApplicationContext`** where **`@EnableTransactionManagement`** is active — most often **service/facade** classes that own business units of work. It also appears on **Spring Data repository** interfaces (built-in or explicit), **integration tests**, and other infrastructure beans (for example Mongo **`MongoTransactionManager`** + service methods). It is **metadata on a class or method**, not a controller-layer default.

## Typical placement in an application

Spring’s `@Transactional` reference allows the annotation on a **class**, **method**, **interface**, or **interface method**. The team recommends annotating **concrete service classes** rather than relying on interface-only metadata — especially for AspectJ weaving, where interface annotations are not inherited.

Layering convention backed by Spring Data JPA docs: define **multi-repository business boundaries** on a **service facade** (`@Transactional` on the service method). Repositories may still carry their own defaults for CRUD/query methods — see [[What is the Transactional annotation in Spring Data]].

```java
@Configuration
@EnableTransactionManagement
class AppConfig { … }

@Service
public class OrderService {

    @Transactional
    public Order place(OrderRequest request) {
        Order order = orders.save(build(request));
        inventory.reserve(order);
        outbox.enqueue(OrderPlaced.from(order));
        return order;
    }
}
```

**Listing 1.** Conceptual service-level boundary — one unit of work across collaborators.

```d2
direction: down
cfg: "@EnableTransactionManagement\n+ TransactionManager bean" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
svc: "@Service\n@Transactional methods" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
repo: "Spring Data repos\n(inherit / declare TX)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
test: "Integration tests\n@Test @Transactional" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

cfg -> svc -> repo
cfg -> test
```

**Fig. 1.** Transaction management must be enabled in the **same context** that declares the annotated beans.

## Other common locations

| Location | Role |
| --- | --- |
| **Service / application layer** | Primary business transaction boundary (facade over repositories) |
| **Repository interfaces** | `SimpleJpaRepository` defaults; add `@Transactional` on custom query/`@Modifying` methods |
| **Integration tests** | Test-managed TX with default rollback — [[What is Transactional used for in tests]] |
| **Data-access services** | e.g. `@Transactional` with `MongoTransactionManager` — [[How do you use multi-document transactions in Spring Data MongoDB]] |

Mechanism everywhere: metadata read by **`TransactionInterceptor`** on a proxy — [[How do you use AOP to manage transactions]], [[What is the Spring Transactional annotation and its parameters]].

> [!warning] Same `ApplicationContext` only
> `@EnableTransactionManagement` discovers `@Transactional` **only in its own context**. Enabling it in a child **`WebApplicationContext`** (for example on `DispatcherServlet`) does **not** advise `@Service` beans in the root context — put transaction management where your services live.

> [!warning] Controllers are a poor default home
> Web handlers should usually delegate to a transactional service. Long TX boundaries on controllers tie up connections and mix web and persistence concerns.

> [!warning] Must be a Spring bean with a visible advised method
> Non-public methods, self-invocation, and calls before the proxy is ready (`@PostConstruct` self-calls) skip the interceptor — [[What happens when one Spring Transactional method calls another]].

> [!tip] Interview answer
> **`@Transactional` goes on Spring beans where you want declarative transaction boundaries — conventionally service/facade methods, plus Spring Data repos and tests.** Enable `@EnableTransactionManagement` and a `PlatformTransactionManager` in that bean’s context. Repositories can be transactional by default; multi-step business work belongs on the service.
