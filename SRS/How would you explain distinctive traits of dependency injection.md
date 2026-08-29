<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# How would you explain distinctive traits of dependency injection?

> [!abstract] Short answer
> Spring’s DI chapter names the traits: the object is **given** collaborators instead of **looking them up**; it does **not** know their **location** or **concrete class**; code is **cleaner** and **decoupling is stronger**; classes are **easier to unit-test** (especially against **interfaces** / abstract types). The injectable type is a **POJO** — no Spring **interfaces, base classes, or annotations** are required. That is what distinguishes DI from **`new`** and from a **service locator**. Constructor injection adds **immutability**, **non-null** required deps, and a **fully initialized** object ([[Why is constructor injection preferred in Spring]]).

## Traits the reference actually lists

After defining DI as constructor / factory-method / property inputs filled by the container, the docs immediately list consequences. Those **are** the distinctive traits ([[How would you explain dependency injection]]):

| Trait | Meaning |
| --- | --- |
| **Passive** | The bean **does not look up** collaborators. |
| **Opaque location** | It does not know **where** the instance came from (JNDI, another package, a mock). |
| **Opaque implementation** | It does not choose the **class** that fulfills the type. |
| **Decoupling** | Composition lives in **metadata** (`BeanDefinition`), not in `new Jdbc…()`. |
| **Testability** | Substitute a stub/mock for an **interface** or abstract type with **no** container. |
| **POJO** | Constructor/setter injection works on ordinary Java; Spring types are optional. |

```java
public class SimpleMovieLister {

	private final MovieFinder movieFinder;

	public SimpleMovieLister(MovieFinder movieFinder) {
		this.movieFinder = movieFinder;
	}
}
```

**Listing 1.** Official constructor-DI example: a POJO with **no** Spring import. The container can inject; so can `new SimpleMovieLister(mockFinder)` in a test.

```d2
Aware: {
  S: InvoiceService
  S -> "BeanFactory.getBean(...)": lookup
}
Passive: {
  Ctx: container
  S2: InvoiceService
  Ctx -> S2: "provides InvoiceRepository"
}
```

**Fig. 1.** Locator-style code still **depends on the registry**. DI’s distinctive move is **push**, not **pull**.

The overview’s `BeanFactory` point is the same trait at framework scale: **decouple configuration and dependency specification from program logic**, instead of hand-rolling Factory / Service Locator in every class.

## Extra traits of the constructor variant

Spring documents **two major variants** (constructor and setter), not Fowler’s “interface injection” as a Framework feature ([[Which dependency injection styles do you know]]). Constructor injection’s extra traits: **`final` fields**, required deps that cannot be `null` after construction, client always sees a **complete** object. A long constructor is a **responsibility** smell, not a DI failure. Setters: **optional** deps, later reconfiguration (for example JMX).

## What is *not* a distinctive trait

**`@Autowired`**, stereotypes, and Boot auto-config are **how Spring finds** candidates. XML `<constructor-arg>` already had the traits above. Field injection **weakens** the POJO story (hidden API, harder `new` in tests).

> [!warning] “Does not know the class” is not “has no type”
> The field is still `MovieFinder`. The trait is: the **lister does not construct or select** `JdbcMovieFinder` vs `StubMovieFinder`. Compile-time coupling to the **abstraction** remains; that is why mocks work.

> [!tip] Interview answer
> Distinctive traits: dependencies are **injected**, not **looked up**; the bean is ignorant of **where** and **which concrete class**; **POJO** + **tests without Spring**; constructor style adds **immutable, complete** objects. That is DI vs locator/`new`, not vs DIP.
