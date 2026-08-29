<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# When is Java configuration more convenient than XML configuration in Spring?

> [!abstract] Short answer
> When the **recipe is Java work**: **constructors**, **if/else**, helpers, JNDI lookups, multi-step setup that would be a **verbose** `<bean>` tree (the same reason the container also offers `FactoryBean` for logic “better expressed in Java”). `@Bean` **is** that Java: the method **instantiates, configures, and initializes** the object — the Java form of `<bean>`. You keep wiring **outside** the application class (like XML), get **compiler-checked** types and `@Bean` **parameters**, and can bootstrap **XML-free** with `AnnotationConfigApplicationContext`. XML stays **more convenient** for **namespaces** and for **rewiring without a rebuild**; `@Configuration` is **not** a 100% XML replacement ([[What configuration styles exist in Spring]], [[Which Spring configuration style do you prefer XML Java or annotations and why]]).

## Java where XML is clumsy; XML where Java cannot replace it

**Java configuration** means **`@Configuration` + `@Bean`** (3.0+), not `@Autowired` on the service class and not `@Component` scan. Those are other styles ([[What is the difference between a Spring configuration class and a component class]]).

Java is the **better fit** when:

| Situation | Why `@Bean` beats `<bean>` |
|---|---|
| **Third-party / library types** | You `new` and configure in a method; you do **not** put `@Component` on code you do not own. FAQ: JavaConfig is **non-invasive** — unlike stereotypes on the target type |
| **Rich construction** | Method body is ordinary Java (args, builders, branching). XML constructors/`factory-method` get long; `FactoryBean` exists for the same “too much XML” case |
| **Type-safe graphs** | `@Bean` parameters are injection points; the **compiler** rejects nonsense types. XML `ref="id"` is a **string** until `refresh()` |
| **One Java entry point** | `@Import` pulls other config classes so you pass **one** type to `AnnotationConfigApplicationContext` ([[How does Import register beans in Spring]]) |
| **XML-free apps** | Same container; metadata is classes, not files |

```java
@Configuration
public class InfraConfig {

	@Bean
	DataSource dataSource() {
		HikariDataSource ds = new HikariDataSource();
		ds.setJdbcUrl("${jdbc.url}");
		ds.setUsername("${DB_USER}");
		return ds;
	}

	@Bean
	InvoiceRepository invoices(DataSource dataSource) {
		return new JdbcInvoiceRepository(dataSource);
	}
}
```

**Listing 1.** Conceptual. Setup lives in Java. Equivalent XML is a `<bean>` plus `<property>` / `<constructor-arg>` and a `ref` string — no compile check that `invoices` needs a `DataSource`.

```d2
direction: down
java: "@Configuration + @Bean\n(Java body, types, @Import)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
xml: "XML namespaces /\nno-recompile wiring" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
mix: "@ImportResource or XML-centric <bean class=Config>" {
  width: 320
  height: 44
  style.fill: "#e3f2fd"
}

java -> mix: "keep a sliver of XML"
xml -> mix: "add @Configuration as needed"
```

**Fig. 1.** Documented choice: Java-centric + `@ImportResource`, or XML-centric + `<bean class="…Config">` with `annotation-config`. Full `@Configuration` still intercepts inter-`@Bean` calls ([[What is lite Bean mode versus full Configuration in Spring]]).

XML is **still** the documented fit when **namespaces** (`tx`, `aop`, …) are the cleanest API, when you must **change wiring without recompiling**, or when a **large XML codebase** should absorb `@Configuration` **as beans** rather than rewrite. Cross-class `ref` without a compiler is **easier in XML**; in Java, declare the collaborator as a **`@Bean` method parameter**.

> [!warning] “Java config” is not `@Component` on the implementation
> Putting `@Service` / `@Autowired` on the class is **annotation injection / scan**. That **touches** source and **decentralizes** wiring — the FAQ’s trade-off versus XML. `@Bean` on `@Configuration` is the XML analogue that **leaves the target class alone**.

> [!warning] `@Configuration` is not a 100% XML replacement
> Namespaces remain **ideal** for some container setup. If you need them, **import** that XML (`@ImportResource`) or stay XML-centric. Do not invent a Java clone of every namespace just to “avoid XML.”

> [!tip] Interview answer
> Java configuration is more convenient when I would otherwise write a large XML construction: @Bean methods are real Java, types are checked, and third-party objects stay unannotated. I still import XML for namespaces and I do not call that a full replacement. Rewiring without a rebuild is still XML’s strength.
