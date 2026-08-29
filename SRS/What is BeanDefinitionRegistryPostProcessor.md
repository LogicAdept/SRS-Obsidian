<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #SRS

# What is BeanDefinitionRegistryPostProcessor?

> [!abstract] Short answer
> `BeanDefinitionRegistryPostProcessor` (since 3.0.1) **extends** `BeanFactoryPostProcessor`. Its extra hook `postProcessBeanDefinitionRegistry(BeanDefinitionRegistry)` runs after regular definitions are loaded and **before** ordinary `BeanFactoryPostProcessor` detection, so you can **register more `BeanDefinition`s** — including definitions of further factory post-processors. No bean **instances** exist yet. The framework type that processes `@Configuration` / `@Bean` / `@Import` this way is `ConfigurationClassPostProcessor`, not an application-facing “parser” SPI.

## Registry phase, then factory phase

`BeanFactoryPostProcessor.postProcessBeanFactory` may **read and change** configuration metadata (`ConfigurableListableBeanFactory`) before the container instantiates any beans other than the post-processors themselves. Classic built-ins: `PropertySourcesPlaceholderConfigurer` (`${…}` in definitions) and `PropertyOverrideConfigurer`. It must **not** call `getBean` to work on instances — that instantiates too early and can skip `BeanPostProcessor`s ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]]).

`BeanDefinitionRegistryPostProcessor` adds a **earlier** method:

- `postProcessBeanDefinitionRegistry` — all **regular** definitions are already in the registry; **no** beans instantiated; you may **add** definitions before the next post-processing phase. That is how later factory post-processors can exist at all if they were not in the original XML/`@Bean` set.
- `postProcessBeanFactory` — inherited. Since Spring Framework **6.1** the interface supplies an **empty default**, because a custom registry post-processor usually only implements the registry method.

`ApplicationContext` auto-detects these beans. Declare a `BeanFactoryPostProcessor` / registry post-processor `@Bean` method as **`static`**, or the declaring `@Configuration` class initializes too early and `@Autowired` / `@PostConstruct` on it can fail.

```java
public class ExtraBeansRegistrar implements BeanDefinitionRegistryPostProcessor {

    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
        registry.registerBeanDefinition(
                "extra",
                BeanDefinitionBuilder.rootBeanDefinition(String.class)
                        .addConstructorArgValue("from-registry")
                        .getBeanDefinition());
    }
}
```

**Listing 1.** Conceptual. Register a definition while the registry is still open; do not look up live beans.

## `@Configuration` uses this SPI

`ConfigurationClassPostProcessor` **is** a `BeanDefinitionRegistryPostProcessor` (and a `PriorityOrdered` factory post-processor). `context:annotation-config` / `context:component-scan` register it ([[What does context annotation-config register]]).

- **Registry step:** `postProcessBeanDefinitionRegistry` **derives further bean definitions** from `@Configuration` classes already in the registry (`@Bean` methods, `@Import` / `ImportBeanDefinitionRegistrar`, component scanning triggered from Java config) ([[How does Import register beans in Spring]]).
- **Factory step:** `postProcessBeanFactory` prepares `@Configuration` classes for runtime by replacing them with **CGLIB-enhanced** subclasses (`ConfigurationClassEnhancer`).

It is **priority-ordered** so those `@Bean` definitions exist **before any other** `BeanFactoryPostProcessor` runs (placeholders and custom factory post-processors must see them). The public type to name is `ConfigurationClassPostProcessor`. `processConfigBeanDefinitions` builds and validates the configuration model; there is no documented application SPI called `ConfigurationClassParser`.

```d2
direction: down
load: "Regular BeanDefinitions loaded" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
bdrpp: "BDRPP.postProcessBeanDefinitionRegistry\n(add more definitions)" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
bfpp: "BFPP.postProcessBeanFactory\n(mutate definitions, e.g. ${…})" {
  width: 320
  height: 70
  style.fill: "#fff8e1"
}
create: "Instantiate beans → BeanPostProcessor" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}

load -> bdrpp
bdrpp -> bfpp
bfpp -> create
```

**Fig. 1.** Registry post-processors run before ordinary factory post-processors; instance post-processors run only after creation ([[What is Spring BeanPostProcessor]]).

> [!warning] Definitions only — no live beans
> Both registry and factory post-processors operate on `BeanDefinition` metadata ([[What is Spring BeanDefinition]]). Instantiating here is a lifecycle violation. Instance work belongs on `BeanPostProcessor`.

> [!warning] Non-static `@Bean` factory post-processors
> A non-static `@Bean` method that returns a `BeanFactoryPostProcessor` forces early creation of the `@Configuration` instance. Use `static`. Lazy-init on the post-processor bean is ignored: if nothing else references it, the context still instantiates it eagerly so it can run.

> [!tip] Interview answer
> BeanDefinitionRegistryPostProcessor extends BeanFactoryPostProcessor with a registry callback that can register extra bean definitions before other factory post-processors run, and before any normal beans exist. ConfigurationClassPostProcessor is the built-in one that turns Java config into definitions, then CGLIB-enhances `@Configuration` classes. Do not confuse that with BeanPostProcessor, which runs on instances later.
