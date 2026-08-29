<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# Which dependency injection styles do you know?

> [!abstract] Short answer
> In Spring, dependencies reach a bean through **constructor injection**, **setter injection**, **field injection**, or **method injection** (multi-arg `@Autowired` methods), plus rarer **lookup method injection**. Official DI is **not** constructors only: the two major variants are **constructor-based** (including **factory-method arguments**) and **setter-based**. **`@Autowired`** / **`@Inject`** can target constructors, fields, setters, or arbitrary methods.

## Injection styles in Spring

| Style | How the container injects | Typical use |
|---|---|---|
| **Constructor** | Calls the constructor with resolved beans | **Required** collaborators; preferred default — [[Why is constructor injection preferred in Spring]] |
| **Setter** | Calls `@Autowired` setter (or XML `<property>`) | **Optional** deps, reconfiguration (JMX), breaking rare constructor cycles |
| **Field** | Sets `@Autowired` private fields directly | Less boilerplate; **discouraged in production** — deps hidden from the API |
| **Method** | `@Autowired` on any method with multiple args | Grouped initialization of several collaborators at once |
| **Lookup** | Container overrides a stub/`abstract` method as `getBean` ([[What is the Lookup annotation in Spring]]) | A **new** instance per call (typically a **prototype**) |

Spring's dependency-injection reference describes **constructor-based** and **setter-based** DI as the two primary forms. **Factory-method arguments** are treated like constructors. **`@Autowired`** (or JSR-330 **`@Inject`**) applies the same resolution rules to fields and methods as well. Field `@Autowired` is convenient but **not** one of those two major variants.

```java
@Service
public class ReportService {

    private final ReportRepository repo;

    @Autowired
    public ReportService(ReportRepository repo) { // constructor
        this.repo = repo;
    }

    @Autowired(required = false)
    public void setMetrics(MeterRegistry metrics) { // setter — optional
    }

    @Autowired
    public void configure(ReportFormatter formatter, Clock clock) { // method
    }
}
```

**Listing 1.** One bean can mix styles; constructor still carries mandatory dependencies.

## XML and factory-method injection (same idea)

Legacy **XML** uses **`<constructor-arg>`** and **`<property>`** — the same constructor vs setter split without annotations.

**`@Bean` factory methods** on `@Configuration` classes are another injection path: arguments to the factory method are **dependencies the container supplies** when creating that bean.

```d2
direction: right
container: "ApplicationContext" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
ctor: "Constructor\n(required deps)" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
setter: "Setter / field\n(optional)" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
bean: "Your @Service" {
  width: 140
  height: 50
  style.fill: "#fce4ec"
}

container -> ctor -> bean
container -> setter -> bean
```

**Fig. 1.** The container resolves collaborators and applies them through the chosen injection style.

> [!warning] Single constructor needs no `@Autowired`
> With **one constructor**, Spring **autowires it by default** — explicit **`@Autowired`** is optional ([[Why is Autowired often omitted on a single constructor in modern Spring]]). With **multiple constructors**, mark one with **`@Autowired`** so the container knows which to use.

> [!warning] “Only constructors” is a style, not a container limit
> Spring **can** inject setters, fields, config methods, factory-method arguments, and lookup methods. Preferring constructors is the **team’s** guidance, not “the container refuses setters.”

> [!warning] Constructor cycles vs setter cycles
> Two beans that each **require** the other in a constructor cannot start (`BeanCurrentlyInCreationException`). Switching one side to a setter (or `ObjectProvider`) is the documented escape hatch, not proof that constructors are unused ([[How does Spring resolve circular dependencies]]).

> [!tip] Interview answer
> Constructor, setter, field, method, plus lookup for a fresh instance per call. Spring’s two major variants are constructor and setter; factory-method args count as constructors. I still use constructors for required dependencies so the object is immutable and complete. Setters or ObjectProvider for optional or later-resolved collaborators. Field injection works but hides the API.
