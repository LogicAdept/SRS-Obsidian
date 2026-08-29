<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is Spring BeanDefinition?

> [!abstract] Short answer
> A **`BeanDefinition`** is the container’s **recipe** for a named bean: configuration metadata the factory uses to **create or acquire** an instance — not the live object ([[What is a Spring bean]]). Inside the IoC container, XML `<bean>`, stereotypes, `@Bean` methods, Groovy, and programmatic registration all become **`BeanDefinition` objects**. The interface is **minimal** on purpose: a `BeanFactoryPostProcessor` should **read and change** class name, property values, scope, and other metadata **before** instances exist ([[What is BeanDefinitionRegistryPostProcessor]]). The bean is what you get after instantiate–inject–initialize.

## Recipe, not the instance

Bean Overview: the container manages beans created from the metadata you supply. **Within the container**, that metadata is `BeanDefinition`. Typical contents:

- **Class** (package-qualified name) — constructor instantiation, or the type that **holds** a static factory method
- **Behavior** — scope, lazy-init, init/destroy method names, `depends-on`
- **Collaborators** — constructor arguments and properties that **ref** other beans ([[How would you explain dependency injection]])
- **Other settings** — pool sizes, autowire mode, `primary` / `fallback` / autowire-candidate flags

Identifiers on the definition must be **unique in that container**. Instantiation from the recipe is constructor, static `factory-method`, instance `factory-bean` + `factory-method`, or a `FactoryBean` ([[How do you create a bean in Spring]]).

```java
BeanDefinition def = BeanDefinitionBuilder
        .rootBeanDefinition(InvoiceService.class)
        .addConstructorArgReference("invoiceRepository")
        .setScope(BeanDefinition.SCOPE_SINGLETON)
        .getBeanDefinition();
registry.registerBeanDefinition("invoiceService", def);
```

**Listing 1.** Conceptual. `BeanDefinitionBuilder` produces a `RootBeanDefinition`. You register a **blueprint**; `getBean("invoiceService")` is the instance. XML `<bean class="…">` fills the same SPI.

Formats only differ in **how** the recipe is written ([[What configuration styles exist in Spring]]). `registerSingleton` can also publish an **already-built** object; that is not a definition-driven recipe and must happen **early** (autowiring / introspection). Registering **new** definitions **while** the factory is serving live traffic is **not** officially supported.

Parent/child definitions (`parent="…"`, `ChildBeanDefinition` / `setParentName`) are **templating**, not Java inheritance. `abstract="true"` means “template only”: `getBean` on that id fails; `preInstantiateSingletons` skips it. Runtime creation uses a **merged** `RootBeanDefinition`. `getBeanClassName()` is for **parsing**; it may be the factory class, empty for an instance factory, or inherited from a parent — not a guaranteed runtime type. `getResolvableType()` is typically complete on that **merged** definition.

`ROLE_APPLICATION` / `ROLE_SUPPORT` / `ROLE_INFRASTRUCTURE` are **hints** for tools, not scopes. Infrastructure definitions (processors, internal helpers) use `ROLE_INFRASTRUCTURE`.

```d2
direction: down
xml: "XML / @Bean / scan / Groovy" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
bd: "BeanDefinition\n(recipe in the registry)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
inst: "bean instance" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}

xml -> bd: readers / scanners
bd -> inst: refresh / getBean
```

**Fig. 1.** Metadata becomes a definition at load/post-process time; the instance appears later ([[How does Spring work under the hood]]).

> [!warning] Changing the instance does not rewrite the recipe
> `BeanFactoryPostProcessor` edits **`BeanDefinition`s**. `BeanPostProcessor` wraps **objects**. After a singleton exists, mutating its definition will not rebuild that cached instance.

> [!warning] Abstract parent without `abstract="true"`
> `ApplicationContext` **eagerly** instantiates singletons. A parent template that has a `class` but is not marked **abstract** is treated as a real singleton and may fail or create an unwanted object.

> [!tip] Interview answer
> BeanDefinition is Spring’s internal recipe: class, scope, constructor args, properties, and lifecycle callbacks. XML, annotations, and Java config all compile into those objects. The container instantiates beans from the recipe. BeanFactoryPostProcessor changes definitions; the live bean is a later step. I do not confuse BeanDefinition with the instance I get from getBean.
