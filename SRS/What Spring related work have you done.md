<!--
reps: 0
priority: 0
-->
#Career/Interview #Career/Experience #Java/Spring/Core #SRS

# What Spring related work have you done?

> [!abstract] Short answer
> Answer with **named Spring projects and shipped behavior**, not the word “Spring.” Official overview: **“Spring”** can mean the **Framework** (IoC, AOP, MVC/WebFlux, JDBC/TX, Test) **or** the **family** (Boot, Security, Data, Cloud, Batch, and others — each with its **own** release). Interviewers hear the family; they score **what you actually ran in production**. Pick **two or three** slices you owned, name the **product**, and say the **problem** it solved ([[What is the Spring ecosystem at a high level]], [[What problems does the Spring Framework address]]). Do **not** invent Cloud or Batch to match a job posting.

## How to answer (not a fake résumé)

This cue is **behavioral**. The Framework cannot document *your* tickets. It **does** document the **labels** you must not mix up.

| Say this product | Only if you actually… |
|---|---|
| **Spring Framework** | Wrote `@Configuration` / `@Component` beans, constructor DI, `@Transactional`, MVC or WebFlux handlers, `spring-test` without Boot |
| **Spring Boot** | `SpringApplication`, starters, auto-config, embedded server, Actuator — **same** `ApplicationContext`, not a second IoC ([[What is the difference between Spring Boot and the core Spring Framework]]) |
| **Spring Data** | Repository interfaces over JPA/JDBC/Mongo, not “I used Hibernate in a servlet” |
| **Spring Security** | Filter chain / method security you configured or extended |
| **Spring Cloud / Batch / AMQP / Integration** | Those **separate** projects — config server, discovery, job chunks, listeners — not “the app ran on Kubernetes” |

**Structure one story:** context (service and traffic) → **which** Spring project → **one** mechanism (DI graph, auto-config you overrode, a `HandlerInterceptor`, a `Repository`, a security filter) → what broke and how you found it (context cache, proxy, circular refs). Then a **second** shorter story in a **different** slice so you are not “the Boot person who never saw the container.”

```java
@RestController
class InvoiceResource {
	private final InvoiceService invoices;

	InvoiceResource(InvoiceService invoices) {
		this.invoices = invoices;
	}

	@GetMapping("/invoices/{id}")
	InvoiceDto get(@PathVariable long id) {
		return invoices.byId(id);
	}
}

@Service
class InvoiceService {
	private final InvoiceRepository repo;

	InvoiceService(InvoiceRepository repo) {
		this.repo = repo;
	}

	@Transactional(readOnly = true)
	InvoiceDto byId(long id) {
		return InvoiceDto.from(repo.findById(id).orElseThrow());
	}
}
```

**Listing 1.** Conceptual **shape** of common Framework+Boot work: web adapter, constructor-injected service, transaction boundary, persistence port. Replace types with **yours**; this is not a claim that you wrote this class.

```d2
direction: down
q: "What Spring work?" {
  width: 200
  height: 36
  style.fill: "#fff3e0"
}
fw: "Framework: IoC, MVC/WebFlux, TX, Test" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
boot: "Boot: starters, auto-config, run" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
sib: "Data / Security / Cloud / Batch / …" {
  width: 300
  height: 40
  style.fill: "#f3e5f5"
}

q -> fw
q -> boot
q -> sib
```

**Fig. 1.** Map stories onto official projects. Effective day-to-day use is still POJOs plus the container ([[How do you work effectively with the Spring framework]]). Tests that need a context belong to `spring-test` / TestContext ([[What is the Spring TestContext Framework]]).

> [!warning] “I have done Spring” is not an answer
> Name **Framework vs Boot vs Data vs Security**. A JAR that only calls `ApplicationContext` is Framework. `SpringApplication.run` is Boot. A discovery annotation is Cloud. Mixing them sounds like a tutorial, not a project.

> [!warning] Annotation bingo is not experience
> Listing `@Autowired`, `@ComponentScan`, and `@SpringBootApplication` without a **failure mode** (wrong bean, proxy self-invocation, auto-config you replaced, test context cache) does not prove you **operated** the stack. Prefer constructor injection and modules you **chose**, not every jar on the classpath.

> [!tip] Interview answer
> I do not say I did Spring in general. On the last service I used Boot to run a Framework ApplicationContext: constructor-injected services, MVC adapters, and Spring Data repositories, with transactions on the service and spring-test for the context. When something failed I looked at the container — auto-config, proxies, bean graphs — not at a magic Boot layer. I only mention Security, Cloud, or Batch if I actually configured those projects.
