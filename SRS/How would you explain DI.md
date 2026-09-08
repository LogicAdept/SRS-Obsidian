<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# How would you explain DI?

> [!abstract] Short answer
> **Dependency injection (DI)** is the process where a type **declares** collaborators (constructor arguments, factory-method arguments, or properties set after construction) and the **container injects** them when it creates the bean. The bean does **not** `new` helpers or look them up. Spring’s two **major** variants are **constructor-based** and **setter-based**; the team **generally advocates constructor injection** for required dependencies. Field `@Autowired` is an extra injection point, not a third classic variant.

## What is injected, and by whom

DI is a **specialized form of IoC**: control of **construction and location** moves out of the bean. `OrderService` knows `OrderRepository`, not `new JdbcOrderRepository()`. The `ApplicationContext` reads `BeanDefinition` metadata and supplies the instance ([[How would you explain dependency injection]], [[What is the difference between dependency injection and inversion of control]]).

```d2
direction: right
bean: "OrderService\ndeclares OrderRepository" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
ctx: "ApplicationContext\ninjects at create time" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
ctx -> bean: "constructor / setter\n/ factory args"
```

**Fig. 1.** The service **uses** the repository; the container **chooses** the implementation.

## Constructor versus setter versus field

| Style | Role |
| --- | --- |
| **Constructor** (and `static` factory arguments) | Mandatory collaborators; `final` fields; bean returned fully initialized. Spring’s preferred default. |
| **Setter** / config method | Optional dependencies with a sane default, or later reconfiguration (JMX). `@Autowired` on a setter can make it required; constructor plus argument checks is still preferable. |
| **Field `@Autowired`** | Container writes a field after construction. Not one of the two official “major” DI variants. Hides the construction contract. |

```java
@Service
public class OrderService {

	private final OrderRepository orders;

	public OrderService(OrderRepository orders) {
		this.orders = orders;
	}
}
```

**Listing 1.** Conceptual. One constructor — from Spring **4.3**, `@Autowired` on that constructor is **unnecessary**; the container still injects it ([[Why is Autowired often omitted on a single constructor in modern Spring]], [[Why is constructor injection preferred in Spring]]).

A **large constructor** is a smell: too many responsibilities, not a reason to switch to field injection ([[Which dependency injection styles do you know]]).

> [!warning] Constructor cycles fail at startup
> Two beans that **each** need the other **only** via constructors produce `BeanCurrentlyInCreationException`. That is a design signal, not “DI is broken”. Setter injection can break the cycle; the reference treats that as a last resort.

> [!tip] Interview answer
> DI means the object declares what it needs and the container pushes those collaborators in — the inverse of `new` or a service locator. Spring’s two main styles are constructor and setter; use constructors for required deps so fields can be final and the bean is complete before use. Since 4.3 a single constructor does not need `@Autowired`.
