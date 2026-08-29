<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# How do you use dependency injection in practice?

> [!abstract] Short answer
> Depend on **abstractions**, expose collaborators on a **constructor**, and let the container **supply** them when it creates the bean. That is the DI chapter’s practice: the class does **not** `new` or look up a locator. Required deps go in the constructor (often **no** `@Autowired` if it is the only one ([[Why is Autowired often omitted on a single constructor in modern Spring]])); optional ones on setters. Register the types as beans ([[How do you create a bean in Spring]]) and wire by type, name, or `@Qualifier` when several match ([[Can you create two singleton beans of the same type in Spring]]). Unit tests call `new InvoiceService(mockRepo)` with **no** Spring.

## Write POJOs, register recipes, let `refresh()` inject

Official DI: objects declare needs only as constructor args, factory-method args, or properties after construction. The container injects at **creation** ([[How can you apply dependency injection with a Spring bean]]). Classes stay free of `BeanFactory` / `ApplicationContext` for routine collaborators — that is why they are easy to **stub**.

**Day-to-day Spring style** the reference already endorses:

- **Constructor** for mandatory collaborators: immutable fields, never `null`, object is complete before anyone else sees it. A long constructor is a **smell** (split the type).
- **Setter / config method** for optional deps with in-class defaults, or third-party types that only have setters, or rare re-injection (JMX).
- **Java-centric** `@Configuration` + `@ComponentScan` for types you own; `@Bean` for types you do not ([[Which Spring configuration style do you prefer XML Java or annotations and why]]). XML `ref` when you need an explicit graph.

```java
@Service
public class InvoiceService {

    private final InvoiceRepository invoices;
    private final TaxCalculator tax;

    public InvoiceService(InvoiceRepository invoices, TaxCalculator tax) {
        this.invoices = invoices;
        this.tax = tax;
    }
}

class InvoiceServiceTest {
    @Test
    void totals() {
        InvoiceService service = new InvoiceService(new FakeInvoices(), new FixedTax());
        // assert…
    }
}
```

**Listing 1.** Conceptual. Production: container injects. Test: you inject. Same constructor.

Do **not** call `getBean` inside `InvoiceService`. Do **not** constructor-inject a cycle; use `@Lazy` / `ObjectProvider` or split types. Field `@Autowired` works but hides the API and blocks `final`.

```d2
direction: down
app: "InvoiceService(repo, tax)" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
prod: "ApplicationContext\ninjects beans" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
test: "new InvoiceService(fake, fake)" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}

app -> prod
app -> test
```

**Fig. 1.** Same injection points; production uses the container, tests do not.

> [!warning] `ApplicationContextAware` is not everyday DI
> Pulling collaborators from the factory in business methods is the **Service Locator** the DI chapter contrasts with. Keep it for framework extension points, not for `InvoiceRepository`.

> [!warning] Two implementations, one type
> Practice is `@Qualifier` / `@Primary` / `@Resource` by name — or do not register both. Hoping `@Autowired` “picks the right one” is how `NoUniqueBeanDefinitionException` shows up in QA.

> [!tip] Interview answer
> In practice I constructor-inject interfaces, register components or @Bean methods, and let Spring wire them at refresh. Tests new the class with fakes. Setters are for optional or third-party APIs. I do not look up beans from the context in application code.
