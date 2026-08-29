<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is a Spring bean?

> [!abstract] Short answer
> A **bean** is an object the **Spring IoC container instantiates, assembles, and manages**. Those objects are the **backbone** of the application in the container’s sense. Any other object (`new` in a DAO, a DTO, a JDK `List`) is **just an object** — not a bean. The container learns **what** to manage from **configuration metadata** (`BeanDefinition`: XML, stereotypes, `@Bean`, Groovy). A bean is **not** required to be a JavaBean with getters/setters; Spring can manage “exotic” classes too. Identity is a **name unique in that container**, plus a **scope** ([[What are Spring bean scopes]]).

## Managed instance vs recipe vs everyone else

`ApplicationContext` **creates, configures, and assembles** beans from metadata. The **definition** is a **recipe**; the **bean** is a live object (or several, if prototype/web-scoped) produced from that recipe ([[How do you create a bean in Spring]]). **Wiring** is how collaborators get into it ([[How would you explain dependency injection]]).

```java
@Service
public class InvoiceService {

	private final InvoiceRepository invoices;

	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** After component scan (or an equivalent `@Bean`), `InvoiceService` is a bean. `Invoice` entities that `invoices.find` **returns** usually are **not** — DAOs and business logic create those outside the container.

```d2
Meta: "BeanDefinition"
Obj: "bean instance"
Other: "new Invoice() in a DAO\n(not a bean)"
Meta -> Obj: instantiate, inject, init
```

**Fig. 1.** Metadata + container → bean. `new` in application code → ordinary Java object.

Typical beans: services, DAOs, infrastructure (`DataSource`, `EntityManagerFactory`), web controllers. **Fine-grained domain objects** are **typically not** registered; AspectJ `@Configurable` is the documented escape hatch for injecting objects born outside the container.

`getBean("id")` on a `FactoryBean` definition returns `getObject()`, which is the bean clients use; the factory itself is another managed object behind `"&"` ([[What is the difference between BeanFactory and FactoryBean]]).

> [!warning] `@Service` without a scan is not a bean
> A stereotype on a class is only a **candidate**. Until `@ComponentScan`, `scan()`, XML `<bean>`, `@Bean`, or `@Import` registers a definition, `getBean` will not find it. Calling `new InvoiceService(...)` in a `@RestController` also **bypasses** the container: that instance is **not** the singleton bean, has **no** injected collaborators, and **no** AOP advice.

> [!tip] Interview answer
> A Spring bean is an object **the IoC container** instantiates, wires, and manages from a **definition**. Everything else in the JVM is just an object. Beans need a unique **name** in that context; they do not need to look like JavaBeans.
