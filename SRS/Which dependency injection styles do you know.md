<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# Which dependency injection styles do you know?

> [!abstract] Short answer
> In Spring, dependencies reach a bean through **constructor injection**, **setter injection**, **field injection**, or **method injection** (multi-arg `@Autowired` methods). The framework supports **constructor-based** and **setter-based** DI as the two major variants; **`@Autowired`** / **`@Inject`** can target constructors, fields, setters, or arbitrary methods.

## The four injection styles in Spring

| Style | How the container injects | Typical use |
|---|---|---|
| **Constructor** | Calls the constructor with resolved beans | **Required** collaborators; preferred default — [[Why is constructor injection preferred in Spring]] |
| **Setter** | Calls `@Autowired` setter (or XML `<property>`) | **Optional** deps, reconfiguration (JMX), breaking rare constructor cycles |
| **Field** | Sets `@Autowired` private fields directly | Less boilerplate; **discouraged in production** — deps hidden from the API |
| **Method** | `@Autowired` on any method with multiple args | Grouped initialization of several collaborators at once |

Spring's dependency-injection reference describes **constructor-based** and **setter-based** DI as the two primary forms. **`@Autowired`** (or JSR-330 **`@Inject`**) applies the same resolution rules to fields and methods as well.

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

> [!tip] Interview answer
> Constructor, setter, field, and method injection. Spring recommends constructor injection for required dependencies — immutable and fully initialized. Setters suit optional deps. Field injection works but hides dependencies. @Autowired and @Inject work on all four; XML uses constructor-arg and property for the same split.
