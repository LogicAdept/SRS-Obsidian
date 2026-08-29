<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #SRS

# What is the relationship between a Spring stereotype component and a Spring bean?

> [!abstract] Short answer
> A **stereotype component** is a **class** marked `@Component` or a **meta-stereotype** of it (`@Service`, `@Repository`, `@Controller`, `@Configuration`, …). That mark makes the type a **scan candidate**. If a scanner (or `@Import` / `register`) **registers** it, the container gets a **`BeanDefinition`** and later **instantiates a bean** — an object it **manages** ([[What is a Spring bean]]). So: **stereotype → (if found) definition → bean**. The reverse is **false**: XML `<bean>`, `@Bean` methods, and `registerSingleton` are beans **without** being stereotype components ([[What is the difference between Bean and Component in Spring]]). A stereotype **without** scan/`@Import` is **not** a bean.

## Marker on a type vs managed instance

`@Component` (since **2.5**) means the annotated class is eligible for **autodetection**. Other stereotypes are `@Component` plus **role** (and sometimes extra runtime behavior, such as `@Repository` exception translation) ([[What happens if you replace Service with Component or Repository on a service class]], [[What is the difference between Repository Component Controller and Service annotations]]). Scanning walks packages you name with `@ComponentScan` and registers matching **concrete** types ([[What is the difference between Component and ComponentScan]]).

```java
@Service
public class InvoiceService { }

@Configuration
public class InfraConfig {
	@Bean
	DataSource dataSource() { return new HikariDataSource(); }
}
```

**Listing 1.** Conceptual. After scan, `InvoiceService` is a **stereotype-sourced bean**. `dataSource` is a **bean** whose recipe is a **factory method**, not a stereotype on `HikariDataSource`. `InfraConfig` itself is **also** a bean because `@Configuration` is a `@Component`.

The **bean** is the live object (or cached singleton) the factory returns for that name. The **stereotype** is only **how the recipe got into the registry**. Default name for a scanned component is the decapitalized class name. Identity is still **name + container**, same as any other bean.

```d2
direction: down
stereo: "@Service InvoiceService\n(stereotype on the class)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
def: "BeanDefinition\ninvoiceService" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
bean: "managed instance" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
other: "@Bean / XML / registerSingleton\n(also beans)" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}

stereo -> def -> bean
other -> def
```

**Fig. 1.** Stereotypes are **one registration path**. Beans are **whatever the container manages** ([[How do you create a bean in Spring]]).

`new Invoice()` in a DAO is **not** a bean, even if `InvoiceService` is a `@Service`. Putting `@Component` on a DTO **and scanning it** would make that DTO a bean — usually a mistake, not a rule that “entities are components.”

> [!warning] Stereotype ≠ already in the context
> `@Component` on the classpath does nothing until `@ComponentScan`, `<context:component-scan>`, `scan()`, or `@Import` of that class. Interviews that say “a component is a bean” skip this step.

> [!warning] Do not call every bean a `@Component`
> `DataSource`, `RestClient`, and many infrastructure objects are beans from **`@Bean` / auto-config / XML**. They are not stereotype components. `@Bean` on a `@Component` class is **lite** factory mode, still a different path than “the class *is* the component.”

> [!tip] Interview answer
> A stereotype component is a class annotated with @Component or a specialization like @Service. Scanning turns that class into a BeanDefinition, then into a managed bean. Every scanned stereotype that is registered is a bean. Many beans are not stereotypes — they come from @Bean methods or XML. Without a scan or Import, the annotation is only a label.
