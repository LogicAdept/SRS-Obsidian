<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Spring/Core/IoC/Configuration #SRS

# How do you create a bean in Spring?

> [!abstract] Short answer
> You do **not** `new` a managed object in application code. You register a **`BeanDefinition` recipe**; the container **creates** (or acquires) the instance when it needs it. **Register** with XML `<bean>`, `@Component` / `@Service` / … plus **component scan**, `@Bean` on `@Configuration`, or a `BeanDefinitionRegistry` (including `BeanDefinitionRegistryPostProcessor`). **Instantiate** with a **constructor**, a **static `factory-method`**, an **instance** `factory-bean` + `factory-method`, or a **`FactoryBean.getObject()`** ([[What is FactoryBean and how do you retrieve the factory itself]]). Then the container applies DI ([[How can you apply dependency injection with a Spring bean]]). XML is still a first-class format — not “legacy only.”

## Recipe first, then construction

“A bean definition is essentially a recipe for creating one or more objects.” Identifiers must be unique in that container. Bootstrap with `ClassPathXmlApplicationContext`, `AnnotationConfigApplicationContext`, and so on ([[Which ApplicationContext implementations are commonly used]]).

**Registration (how the recipe gets in):**

| Style | What you write |
| --- | --- |
| XML | `<bean id="exampleBean" class="examples.ExampleBean"/>` |
| Stereotypes | `@Component` (and `@Service`, `@Repository`, `@Controller`, …) + `@ComponentScan` / `<context:component-scan>` |
| Java config | `@Bean` method on `@Configuration` (typical for types you do not own, or multi-step setup) |
| Programmatic | `registry.registerBeanDefinition(…)` / `GenericApplicationContext` + a reader |

`@Configuration` / `@Bean` / `@Import` are parsed by `ConfigurationClassPostProcessor` ([[What is BeanDefinitionRegistryPostProcessor]]). Scan and `@Bean` can live together.

**Instantiation (how the object is born)** — from Instantiating Beans:

1. **Constructor** — container `new`s the `class` (any normal type; not limited to JavaBeans).
2. **Static factory** — `class` is the type that **holds** the method; `factory-method="createInstance"`.
3. **Instance factory** — omit `class`; `factory-bean="locator"` + `factory-method="createClientServiceInstance"` on an **existing** bean.
4. **`FactoryBean`** — the definition is the factory; `getBean("id")` is the **product**.

```java
@Configuration
@ComponentScan("example.app")
public class AppConfig {

    @Bean
    DataSource dataSource() {
        return new ExampleDataSource();
    }
}

@Service
public class InvoiceService {
    public InvoiceService(InvoiceRepository repo) { /* DI */ }
}
```

**Listing 1.** Conceptual. Scan creates `InvoiceService`; `@Bean` creates `DataSource`. Both are beans.

```xml
<bean id="clientService" class="example.ClientService" factory-method="createInstance"/>
<bean id="accountService" factory-bean="serviceLocator" factory-method="createAccountServiceInstance"/>
```

**Listing 2.** Conceptual. Static factory vs instance factory. Not the same as implementing `FactoryBean`.

```d2
direction: down
reg: "register BeanDefinition" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
inst: "instantiate\n(ctor / factory / FactoryBean)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
di: "inject collaborators" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}

reg -> inst
inst -> di
```

**Fig. 1.** Creating a Spring bean is register-then-construct, not `new` in a servlet.

> [!warning] XML is not retired
> The IoC reference still teaches XML as configuration metadata. `@Configuration` is **not** a 100% replacement (namespaces, `@ImportResource`). Saying “only annotations in new projects” is a team convention, not a container rule.

> [!warning] `factory-bean` vs `FactoryBean`
> XML `factory-bean` / `factory-method` call a method on **another bean**. `org.springframework.beans.factory.FactoryBean` is a **type** whose `getObject()` is the exposed instance. Mixing the two names is a classic interview miss.

> [!tip] Interview answer
> I register a bean definition — XML, stereotype plus scan, or @Bean on configuration — and Spring instantiates it with a constructor, a factory method, or a FactoryBean. I do not new the object myself. @Bean is especially useful for third-party types; @Component is for classes I own.
