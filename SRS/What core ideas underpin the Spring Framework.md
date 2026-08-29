<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# What core ideas underpin the Spring Framework?

> [!abstract] Short answer
> Spring’s own introduction: **handle infrastructure so you write the application** — **POJOs** with **enterprise services applied non-invasively** (a method can be transactional, a JMS handler, or a JMX operation **without those APIs in the method**). **IoC / DI** composes those objects instead of `new` or a locator. **AOP** attaches cross-cutting behavior through **proxies** (or AspectJ) without scattering it in domain types. The stack is **modular** (use the container, JDBC, or MVC **alone**). **Non-invasiveness** is a stated tenet: domain code **need not** depend on Spring types; when it does, that is a **choice**. Spring is **not** a full Jakarta EE server; it **integrates** selected specs ([[What is the Spring Framework]]).

## Infrastructure around ordinary objects

Overview line: the Framework is a Java platform of **infrastructure**. You assemble **plain objects**; the container and modules supply persistence, transactions, messaging, web. Domain logic is **non-intrusive** — generally **no** `ApplicationContext` in business methods. Integration layers may depend on JDBC/JPA **and** Spring; isolate that from the rest of the codebase.

```d2
POJO: "application types"
IoC: "IoC container\ncreate + inject"
AOP: "AOP / @Transactional"
Mod: "optional modules\njdbc, web, test"
IoC -> POJO: wires
AOP -> POJO: advises
Mod -> POJO: templates / MVC
```

**Fig. 1.** Core ideas: **composition** (IoC), **cross-cutting** (AOP), **optional modules**, all aimed at **POJOs**.

| Idea | What it buys |
| --- | --- |
| **IoC / DI** | Collaborators **declared**, **injected** at creation — tests `new Service(mock)` ([[How would you explain dependency injection]]) |
| **Non-invasiveness** | No requirement to implement Spring interfaces in the domain; `InitializingBean` / `*Aware` are **opt-in** for infrastructure |
| **AOP** | `@Transactional` and similar as **proxies**; 80% of enterprise AOP without a full AspectJ rewrite ([[What is an AOP proxy in Spring]]) |
| **Templates / abstractions** | `JdbcTemplate` (and kin) so you do not own connection/exception boilerplate; swap a persistence provider in **config** |
| **Modularity** | IoC under **another** web stack; JDBC without MVC |
| **Choice** | XML vs Java vs scan; Spring AOP vs AspectJ; not one true architecture ([[How do you work effectively with the Spring framework]]) |

```java
public class InvoiceService {

	private final InvoiceRepository invoices;

	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** The DI chapter’s POJO: **no** Spring type on the class. `@Service` / `@Transactional` are optional metadata, not the core idea.

The IoC component **codifies** Factory / Builder / locator **patterns as container features** so every team does not re-implement them. AOP’s “central tenet” restates non-invasiveness: you are **not forced** to put framework types in the domain; some APIs exist because they are **easier to read** in infrastructure code.

**Not** a core Framework idea: Boot’s convention-over-configuration (a **documented on-ramp on top of** the Framework). **Not** “Spring is EJB.”

> [!warning] Non-invasive is a default, not a ban
> `ApplicationContextAware`, `BeanPostProcessor`, and `@Configuration` **are** Spring APIs. The idea is: **keep them off the domain**. Putting `getBean` in `InvoiceService` abandons IoC. Putting `@Transactional` on a service is the **intended** non-invasive transaction example.

> [!tip] Interview answer
> Spring is built on **IoC**, **POJOs**, **non-invasive services** (especially **AOP**/transactions), **portable templates**, and **modules you opt into**. You focus on application types; the Framework supplies the wiring and the enterprise plumbing — it does not replace the language or a full app server.
