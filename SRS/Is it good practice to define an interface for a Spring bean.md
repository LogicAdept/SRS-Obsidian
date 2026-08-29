<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Framework/AOP #SRS

# Is it good practice to define an interface for a Spring bean?

> [!abstract] Short answer
> **Often yes for collaborators you inject and test; not a rule for every `@Component`.** Spring **advocates programming to interfaces** (AOP docs: “best to program to interfaces rather than classes”) but is **not prescriptive** — CGLIB can advise a class with **no** business interface. DI is more effective when the dependency type is an **interface or abstract class** (stubs/mocks, swap implementations in config). An interface is **noise** when there is one implementation, no proxy advice, and no second impl. It becomes **important** when `@Transactional` / AOP uses a **JDK dynamic proxy**: inject the **interface**, not the concrete class.

## Why interfaces show up in Spring’s own advice

The DI chapter’s testability trait: the bean does not know the **class** of a collaborator; mocks work when you depend on an **abstraction** ([[How would you explain distinctive traits of dependency injection]]). The container still creates a **class** bean (`JdbcInvoiceRepository`); injection points should usually be typed as `InvoiceRepository`.

Spring AOP: if the target implements **at least one** interface, the default Framework proxy is a **JDK dynamic proxy of those interfaces**; if **none**, a **CGLIB** subclass ([[What is an AOP proxy in Spring]]). “While it is best to program to interfaces rather than classes, the ability to advise classes that do not implement interfaces can be useful when working with legacy code.”

```java
public interface InvoiceRepository {
	Invoice find(long id);
}

@Service
public class JdbcInvoiceRepository implements InvoiceRepository { /* ... */ }

@Service
public class BillingService {
	public BillingService(InvoiceRepository invoices) { this.invoices = invoices; }
	private final InvoiceRepository invoices;
}
```

**Listing 1.** Interface on the **injection point**. The `@Service` implementation is the bean class. Tests: `new BillingService(mockRepo)` with no Spring.

```d2
Client: BillingService
Iface: InvoiceRepository
Jdbc: JdbcInvoiceRepository
Tx: "JDK proxy (interfaces)"
Client -> Iface: injects
Jdbc -> Iface: implements
Tx -> Iface: "proxy implements"
```

**Fig. 1.** Clients depend on the interface. A JDK proxy **is** that interface; it is **not** `JdbcInvoiceRepository`.

## When you can skip a dedicated interface

Spring does **not** require an interface to be a bean. Controllers, `@Configuration`, and tiny helpers with a single impl and **no** class-level advice are fine as concrete types. Empty `IFoo` / `FooImpl` pairs that never get a second implementation or a mock do not make the design “more Spring.”

Multiple beans of the same interface still need `@Qualifier` / `@Primary` ([[Can you create two singleton beans of the same type in Spring]]). The interface did not remove that.

**Boot** often sets **class-based** proxies (`spring.aop.proxy-target-class`), so missing an interface does not block `@Transactional`. Framework default remains **JDK when interfaces exist**. Either way, **self-invocation** on `this` skips advice whether or not you have an interface ([[What are Spring AOP proxy limitations]]).

> [!warning] Injecting the concrete class under a JDK proxy
> If `BillingService` takes `JdbcInvoiceRepository` and that bean is JDK-proxied, the object in the factory **implements the interfaces only**. Type matching / casts to the **class** fail. Inject `InvoiceRepository`, or force CGLIB (`proxyTargetClass=true`). Marker interfaces (e.g. `Serializable`) also count as “has an interface” and can flip you onto JDK proxies unexpectedly.

> [!tip] Interview answer
> Good practice for **injected, mocked, or multi-impl** types and for **JDK-proxied** services. Not mandatory for every bean. Spring prefers interfaces, still advises concrete classes when needed, and does not force a 1:1 `I*` for each `@Component`.
