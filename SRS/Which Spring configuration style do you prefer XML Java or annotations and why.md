<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# Which Spring configuration style do you prefer: XML, Java, or annotations — and why?

> [!abstract] Short answer
> The Framework’s own FAQ is **“it depends.”** XML, annotation-driven injection, classpath stereotypes, and Java `@Configuration` / `@Bean` are **all first-class**; the container is **decoupled from the metadata format** and is built to **mix** them. A defensible modern default is **Java-centric**: `@Configuration` for infrastructure and third-party types (no source change on those classes), **constructor injection** on your types, **component scan** for application stereotypes, and **`@ImportResource` only** for XML namespaces that still earn their keep. That is a **preference**, not a rule — Boot’s getting-started path matches it; large XML codebases can stay XML-centric and pull in `@Configuration` as beans.

## Three different “annotation” stories

Interview dumps collapse three mechanisms:

1. **XML bean definitions** — explicit `<bean>`, `ref`, namespaces (`tx`, `aop`, …). Wires **without** editing or recompiling the class. The reference still says `@Configuration` is **not** a 100% XML replacement; namespaces remain an **ideal** fit for some container setup. Bootstrap with `ClassPathXmlApplicationContext`, or stay Java-centric and import XML ([[Which ApplicationContext implementations are commonly used]]).
2. **Annotation-based injection (2.5+)** — `@Autowired` / `@Inject` / `@Resource` on fields and methods. This **does not register** the bean by itself. `<context:annotation-config/>` (or Boot / `AnnotationConfigApplicationContext`) installs the processors ([[What does context annotation-config register]]). Beans still come from XML, `@Bean`, or a scan.
3. **Java configuration (3.0+)** — `@Configuration` + `@Bean` (and `@Import`, `@ComponentScan`) define beans **outside** the application class, with compiler and refactoring support. Inter-`@Bean` calls on a **full** `@Configuration` class go through the container (CGLIB); a `@Bean` on a plain `@Component` is **lite** mode.

Classpath **`@Component` / `@Service` / …** scanning is a fourth registration style: the type **is** the definition. Concise, but wiring is **decentralized** and the class is no longer a pure unaware POJO.

```java
@Configuration
@ImportResource("classpath:tx-namespace.xml")
@ComponentScan("example.app")
public class AppConfig {

    @Bean
    DataSource dataSource() {
        return new ExampleDataSource();
    }
}

@Service
public class InvoiceService {
    public InvoiceService(InvoiceRepository repo) { /* … */ }
}
```

**Listing 1.** Conceptual. Java-centric entry: scan your types, `@Bean` what you do not own, keep a sliver of XML if a namespace is still the cleanest API.

Annotation injection runs **before** XML property injection; XML **wins** if both set the same property. Pick one story per dependency.

```d2
direction: down
meta: "configuration metadata" {
  width: 220
  height: 36
  style.fill: "#e3f2fd"
}
xml: "XML / namespaces" {
  width: 180
  height: 36
  style.fill: "#fff3e0"
}
ann: "@Autowired on a type" {
  width: 200
  height: 36
  style.fill: "#f3e5f5"
}
java: "@Configuration @Bean" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
scan: "@Component scan" {
  width: 160
  height: 36
  style.fill: "#eceff1"
}
ctx: "ApplicationContext" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}

meta -> xml
meta -> java
xml -> ann
scan -> ann
java -> ctx
xml -> ctx
scan -> ctx
ann -> ctx
```

**Fig. 1.** Same container; four metadata paths. `@Autowired` is wiring, not an alternative to `@Bean`.

> [!warning] Do not answer “annotations” as one bucket
> `@Service` + scan, `@Autowired` on an XML-defined bean, and `@Bean` on `@Configuration` are **different** features. Saying “I prefer annotations” without that split is the usual fail.

> [!warning] Mixing without an entry point
> You can combine styles, but production still has **one** bootstrap: XML files **or** `@Configuration` classes as the root, then `@ImportResource` / `<bean class="…Config">` / component-scan to pull the rest. Two competing roots are how duplicate beans and override surprises appear.

> [!tip] Interview answer
> Spring does not pick a winner: XML is best when you must wire without touching source, stereotypes are concise for your own types, and @Configuration is the type-safe way to declare infrastructure beans. I default to Java-centric config plus constructor injection, and I import XML only for namespaces. Mixing is supported; I keep a single entry point so overrides stay predictable.
