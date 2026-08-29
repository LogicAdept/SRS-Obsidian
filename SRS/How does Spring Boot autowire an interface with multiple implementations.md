<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS

# How does Spring Boot autowire an interface with multiple implementations?

> [!abstract] Short answer
> `@Autowired` is **by type**. Two `@Service` classes that implement `MyService` make a **single-valued** `MyService` injection fail (`NoUniqueBeanDefinitionException`) unless you narrow it: **`@Qualifier`**, **`@Primary`** / **`@Fallback`** (Framework 6.2), or a **parameter name** that matches a bean name (`-parameters`). Inject **all** implementations as **`MyService[]`**, **`List`/`Set`**, or **`Map<String, MyService>`** (keys = **bean names**). This is Spring IoC, not a Boot-only feature.

## Type match first, then a tie-breaker

Both implementations are beans. A constructor `MyService myService` asks for **one** candidate. Spring does **not** pick arbitrarily ([[How do you choose among several matching beans with Primary and Qualifier]]).

```java
@Service
@Qualifier("first")
class FirstService implements MyService { }

@Service
@Qualifier("second")
class SecondService implements MyService { }

@Component
class FirstManager {
	private final MyService myService;

	FirstManager(@Qualifier("first") MyService myService) {
		this.myService = myService;
	}
}
```

**Listing 1.** Type-level `@Qualifier` on a scanned `@Component` / `@Service` is the documented alternative to XML `<qualifier>`. The injection-point `@Qualifier` **narrows the type matches**. Qualifier strings need not be unique when you inject a **collection** — they **filter**. Bean **name** is a **fallback** qualifier (`@Service("first")` or a parameter named `firstService` matching bean `firstServiceImpl` only if the names actually match). Prefer semantic values (`main`, `action`), not “the id.” `@Resource(name = "…")` is **by unique name** and does **not** apply to constructors ([[How do you select a Spring bean using application properties]]).

```java
@Bean
@Primary
MyService firstService() { return new FirstService(); }
```

**Listing 2.** `@Primary` on exactly **one** candidate fills a **single-valued** `MyService`. Two primaries still fail. `@Fallback` on the others leaves one “regular” bean, which is then treated as primary. **`@Primary` does not pick among `List`/`Map` elements.**

```java
@Component
class SecondManager {
	private final List<MyService> myServices;
	private final Map<String, MyService> byName;

	SecondManager(List<MyService> myServices, Map<String, MyService> byName) {
		this.myServices = myServices;
		this.byName = byName;
	}
}
```

**Listing 3.** Official multi-bean injection: array, `List`/`Set`, or `Map<String, …>`. Map keys are **bean names** (`firstService`, `secondService` by default from the class name). Order: `Ordered` / `@Order` / `@Priority`; otherwise **registration order**. `@Order` on a `@Configuration` class does **not** order that class’s `@Bean` methods. Empty collections: a **single constructor** may receive an **empty** list; a required **field** `List<MyService>` still expects **at least one** element.

```d2
direction: down
impls: "FirstService + SecondService\nboth MyService" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
one: "MyService one\nQualifier / Primary / name" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
all: "List or Map<String, MyService>\nall candidates" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

impls -> one
impls -> all
```

**Fig. 1.** Same beans, two injection shapes. Parameter-name matching (6.1+) needs **`javac -parameters`**. Nested types inside `@SpringBootApplication` still work if they are `@Component`s, but they are not how Boot “autowires interfaces.”

> [!warning] `@Qualifier` on the class is not `@Service("id")`
> `@Qualifier("first")` labels the bean for **type+qualifier** matching. The default bean name of class `FirstService` is still **`firstService`**. Mixing a qualifier string with a different `@Service("…")` id is a common miss. `@Autowired` on a constructor is optional when there is **only one** constructor.

> [!warning] Two implementations and a bare `MyService` field will not start
> That is **`NoUniqueBeanDefinitionException`**, not a random first `@Service`. `@Inject` follows the same type rules. Do not disable autowiring (`autowireCandidate = false`) unless you intend the bean to be **unreachable** by type.

> [!tip] Interview answer
> Autowire is by type. Several implementations of one interface are fine for List or Map keyed by bean name. For a single MyService I add @Qualifier or @Primary. @Qualifier on the implementation class is valid with component scan. I do not expect Spring Boot to pick a winner by itself.
