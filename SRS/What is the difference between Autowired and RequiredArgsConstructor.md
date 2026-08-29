<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Methodologies/Principles/DependencyInjection #Java/Annotations #SRS

# What is the difference between Autowired and RequiredArgsConstructor?

> [!abstract] Short answer
> **`@Autowired` is Spring.** It marks an **injection point** (constructor, field, setter, config method, parameter) so `AutowiredAnnotationBeanPostProcessor` **resolves beans by type** (then `@Qualifier` / `@Primary`). **`@RequiredArgsConstructor` is Lombok**, not Spring: at compile time it **generates a constructor** for uninitialized **`final`** fields and **`@NonNull`** fields (plus a null-check for those `@NonNull` parameters). It does **not** look up the container. If that generated constructor is the **only** one, Spring **autowires it anyway** and you omit `@Autowired` ([[Why is Autowired often omitted on a single constructor in modern Spring]]). They **stack**: Lombok writes the constructor Spring prefers ([[Why is constructor injection preferred in Spring]]).

## Spring injection vs a generated constructor

Dump text that treats them as two injection engines is wrong. Field `@Autowired` runs in **populate** (after `new`). Constructor injection (hand-written or Lombok) runs **while the instance is created**. `@Autowired` also works on **methods** ([[Can Autowired be applied to methods other than constructors and setters]]). Several types → `@Qualifier` / `@Primary` on the **injection point** — Lombok does not choose among beans.

```java
@Service
public class BillingService {
    @Autowired
    private InvoiceRepository invoices; // field injection — not final, harder to unit-test
}

@Service
@RequiredArgsConstructor
public class BillingService {
    private final InvoiceRepository invoices; // Lombok ctor; Spring injects the only constructor
}
```

**Listing 1.** Conceptual. Same collaborator. Left: Spring annotation on the **field**. Right: **no** `@Autowired`; Lombok emits `BillingService(InvoiceRepository)` and Spring 4.3+ uses it.

Lombok parameter order follows **field declaration order**. `@NonNull` fields that are **not** initialized at declaration get a parameter and an NPE if the argument is null. **Static** fields are skipped. An **explicit** constructor does **not** suppress generation — you can end up with **two** constructors; then Spring needs `@Autowired` on the injection one (`onConstructor` is experimental) or you drop the extra ctor.

`staticName = "of"` makes the real constructor **private** and adds a **static factory**. Spring’s default constructor autowiring will **not** see a usable public injection constructor unless you also declare `factory-method`.

```d2
direction: down
lombok: "@RequiredArgsConstructor\n(compile: generate ctor)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
spring: "@Autowired / single-ctor rule\n(runtime: resolve beans)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
bean: "BillingService instance" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}

lombok -> spring -> bean
```

**Fig. 1.** Lombok is bytecode. Spring still does matching (`required = true` by default, [[What does Autowired required false do]]).

Unit tests: `new BillingService(mockRepo)` works for **any** constructor, Lombok or not. Field `@Autowired` needs the container, `ReflectionTestUtils`, or package-visible setters. That is why dumps call Lombok “easier to test” — they mean **constructor injection**, not a Lombok-specific DI feature.

> [!warning] `@Autowired` is not “assign fields after every bean exists”
> The container does **not** wait to finish **all** singletons before injecting this bean. It instantiates a bean, injects **its** collaborators (creating them first if needed), then continues. Field injection is just **one** `@Autowired` target, and it is **not** the recommended style for required deps.

> [!warning] A second constructor silently changes the rules
> `@Data` / `@NoArgsConstructor` plus `@RequiredArgsConstructor` can yield a **no-arg** constructor **and** the required one. With **no** `@Autowired`, multi-constructor resolution may pick the **wrong** ctor or fail. Keep **one** injection constructor. Copy `@Qualifier` onto **parameters** (`lombok.copyableAnnotations` or write the ctor) — a qualifier only on the **field** is not what constructor matching reads.

> [!tip] Interview answer
> Autowired is Spring’s injection marker. RequiredArgsConstructor is Lombok generating a constructor for final and NonNull fields. Spring then autowires that constructor, usually without Autowired if it is the only one. I do not treat Lombok as an alternative to Autowired matching — Qualifier and Primary still apply — and I do not use field Autowired when a constructor will do.
