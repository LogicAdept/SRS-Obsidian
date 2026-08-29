<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# Why is constructor injection preferred in Spring?

> [!abstract] Short answer
> **Constructor injection** makes required dependencies explicit, allows **`final`** fields, guarantees a **fully initialized** bean before use, and is what the **Spring team recommends** for mandatory collaborators. **Field injection** hides dependencies and complicates plain unit tests; **setter injection** fits **optional** dependencies with defaults.

## What Spring recommends

The Spring Framework reference states that the team **generally advocates constructor injection** because it:

- lets components be **immutable** (`final` dependency fields)
- ensures **required dependencies are not `null`**
- returns beans to callers in a **fully initialized state**

Spring Boot’s reference likewise recommends **constructor injection** to wire dependencies.

Use **constructors for mandatory** dependencies and **setters (or `@Autowired(required = false)`) for optional** ones. Setter injection also supports reconfiguration later (for example JMX-managed beans).

```java
@Service
public class OrderService {

    private final OrderRepository orders;
    private final PaymentGateway gateway;

    public OrderService(OrderRepository orders, PaymentGateway gateway) {
        this.orders = orders;
        this.gateway = gateway;
    }
}
```

**Listing 1.** Single constructor — dependencies are visible in the signature and can be `final`. When only one constructor exists, **`@Autowired` is optional**.

## Compared with field and setter injection

| Style | Strength | Drawback |
|---|---|---|
| **Constructor** | Explicit contract, immutability, full initialization | Many constructor args may signal too many responsibilities |
| **Field `@Autowired`** | Less boilerplate | Dependencies not visible in the public API; needs container or reflection to inject in tests |
| **Setter** | Good for optional / reconfigurable deps | Object exists before all deps are set unless you add null checks |

Field injection is discouraged in **production** code because dependencies are not part of the type’s public construction contract. In tests, Spring’s own guidance treats field injection as more natural — but that is a testing convenience, not a production pattern.

```d2
direction: right
ctor: "Constructor injection\n(all deps at create time)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
field: "Field injection\n(container sets private fields)" {
  width: 220
  height: 80
  style.fill: "#fce4ec"
}
setter: "Setter injection\noptional / late deps" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}

ctor -> field: "preferred for\nrequired deps"
setter -> field: "for optional deps"
```

**Fig. 1.** Mandatory collaborators belong in the constructor; setters cover optional configuration.

> [!warning] Constructor cycles fail at startup
> **Pure constructor injection** cannot resolve a circular dependency (`A` needs `B`, `B` needs `A`) — the container throws **`BeanCurrentlyInCreationException`**. That surfaces design problems early. Setter injection can break the cycle (one bean injected before fully initialized), but the reference treats that as a last resort, not the default design.

See [[Which dependency injection styles do you know]] and [[Why is Autowired often omitted on a single constructor in modern Spring]].

> [!tip] Interview answer
> Constructor injection is preferred because dependencies are explicit, can be final, and the bean is fully built before use — Spring’s own recommendation for required deps. Field injection hides collaborators and is awkward to test without the container. Use setters for optional dependencies; with one constructor you often skip @Autowired entirely.
