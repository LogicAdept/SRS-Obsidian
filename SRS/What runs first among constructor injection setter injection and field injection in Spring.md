<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #Java/Annotations #SRS

# What runs first among constructor injection, setter injection, and field injection in Spring?

> [!abstract] Short answer
> **Constructor first** — that **is** instantiation: the container cannot populate a bean that does not exist yet (`createBeanInstance` / constructor or factory-method arguments). **Then fields, then setters (config methods).** `@Autowired` javadoc: **“Fields are injected right after construction of a bean, before any config methods are invoked.”** Setters are a **special case of config methods** and run in that **later** populate pass, together with other `@Autowired` methods ([[Can Autowired be applied to methods other than constructors and setters]]). XML `<property>` is the same **after-construct** window. `@PostConstruct` / `afterPropertiesSet` run **after** all of this ([[In what order does Spring initialize a bean and its dependencies]]).

## Instantiate, then populate

You can **mix** all three on one class. Order on **that instance**:

1. **Constructor** (or factory-method args) — required deps can be `final`.
2. **`@Autowired` fields** — not `final`; not part of the type’s public API.
3. **`@Autowired` setters / config methods** — and XML `<property>` / autowire-by-name/type in `populateBean`.

```java
@Service
public class BillingService {
	@Autowired
	private AuditLog audit;          // 2. field

	private final InvoiceRepository invoices;
	private Notifier notifier;

	public BillingService(InvoiceRepository invoices) { // 1. constructor
		this.invoices = invoices;
	}

	@Autowired
	public void setNotifier(Notifier notifier) { // 3. setter
		this.notifier = notifier;
	}
}
```

**Listing 1.** Conceptual. In the constructor, `audit` and `notifier` are still unset. In `@PostConstruct`, all three are injected.

```d2
direction: down
ctor: "constructor / factory-method" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
field: "@Autowired fields" {
  width: 220
  height: 36
  style.fill: "#fff3e0"
}
set: "setters / config methods / XML property" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
init: "Aware → @PostConstruct → init" {
  width: 260
  height: 40
  style.fill: "#f3e5f5"
}

ctor -> field -> set -> init
```

**Fig. 1.** Construction before `populateBean`. Fields before config methods ([[Which dependency injection styles do you know]]).

Constructor cycles **cannot** start (`BeanCurrentlyInCreationException`). Setter/field cycles can use an **early** singleton when circular references are allowed — another reason constructors run in a **different** phase ([[How does Spring resolve circular dependencies]]). Team preference is still **constructor for required** deps ([[Why is constructor injection preferred in Spring]]); that is **not** the same question as order.

> [!warning] Dump answered “why constructor is better”
> Immutability, SRP, tests without Spring are **true** for preference, **not** the injection **sequence**. Constructor injection does **not** make every cycle impossible if the class **also** has setter/field injection into a loop.

> [!warning] Constructor body is too early for field/setter collaborators
> Do not call `audit` from the constructor. Use `@PostConstruct` or a method after populate. `@Autowired` on a **parameter** of a production constructor is largely **ignored** by core (except tests); put `@Autowired` on the **constructor** or rely on the single-ctor rule.

> [!tip] Interview answer
> Constructor injection runs first because that is how the instance is created. Then Spring injects @Autowired fields, then setter and other config methods. Init callbacks run after that. I do not use field injection in a constructor, and I do not confuse this order with “constructors are preferred.”
