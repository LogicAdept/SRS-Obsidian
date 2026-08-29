<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #SRS

# What is the Spring Service annotation?

> [!abstract] Short answer
> **`@Service` (2.5)** is a **`@Component` specialization** for the **service layer**: classpath scanning treats it as a bean candidate, same as `@Component`. Javadoc: Evans DDD **service** (“operation offered as an interface that stands alone in the model, with no encapsulated state”) or a J2EE **business façade**. Teams may **narrow** the meaning; Spring does **not** add a service interceptor today. Scanning docs: if you choose between `@Component` and `@Service` for that layer, **`@Service` is clearly the better choice** (tools, AOP pointcuts, possible **future** semantics). **`value`** aliases `Component.value` (bean name). Without `@ComponentScan` / `@Import` / `register`, it is **not** a bean ([[What is the relationship between a Spring stereotype component and a Spring bean]]).

## Label + scan, not extra runtime

`@Service` is **meta-annotated with `@Component`**, so the default include filters pick it up ([[What is the Spring ComponentScan annotation]]). Default scope is **singleton**. Default id is the decapitalized class name unless `value` is set.

```java
@Service("billing")
public class InvoiceService {
	private final InvoiceRepository invoices;
	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** Conceptual. After scan, bean name `billing`. Constructor injection does not need `@Autowired` on a single constructor. `@Transactional` is **separate** — `@Service` does not start transactions.

Compared with siblings ([[What is the difference between Repository Component Controller and Service annotations]]): `@Component` is generic; `@Repository` adds **exception translation**; `@Controller` is what MVC **handler mapping** looks for. Swapping `@Service` for `@Component` still registers the class; you lose the **service** pointcut ([[What happens if you replace Service with Component or Repository on a service class]]).

```d2
direction: down
scan: "@ComponentScan" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
svc: "@Service InvoiceService" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
bean: "singleton bean" {
  width: 160
  height: 36
  style.fill: "#fff3e0"
}

scan -> svc -> bean
```

**Fig. 1.** Stereotype on the **type**; the **bean** is the managed instance. `@Bean` factory methods are a different registration path.

> [!warning] `@Service` is not `@Transactional` and not a controller
> A class with `@GetMapping` but only `@Service` is **not** a mapped MVC handler. A façade that talks to JPA still is **not** `@Repository` unless it **is** the persistence adapter.

> [!warning] No scan → no bean
> The annotation only **classifies** the type. The container must **find** it. Putting `@Service` on a DTO you also `new` in a DAO creates a **second**, unmanaged instance.

> [!tip] Interview answer
> @Service is a @Component for the business layer: DDD service or façade, found by component scan, no extra interceptor unlike @Repository. I use it instead of bare @Component so pointcuts and tools see a service. It does not mean transactions or web mappings.
