<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS

# What is the difference between BeanFactoryPostProcessor and BeanPostProcessor?

> [!abstract] Short answer
> **`BeanFactoryPostProcessor` edits recipes; `BeanPostProcessor` edits instances.** A BFPP’s `postProcessBeanFactory(ConfigurableListableBeanFactory)` runs when **all definitions are loaded and no ordinary beans exist yet** — you change `BeanDefinition` property values (classic: `PropertySourcesPlaceholderConfigurer` replacing `${…}`). A BPP’s `postProcessBeforeInitialization` / `postProcessAfterInitialization` run **after** that bean is **constructed and populated**; you may **wrap a proxy** (AOP / `@Transactional`) ([[What is Spring BeanPostProcessor]]). Javadoc: a BFPP must **never** work on instances (`getBean` here instantiates too early and can **skip** later BPPs). `ApplicationContext` **auto-detects** both; a plain `BeanFactory` does not ([[What is the difference between BeanFactory and ApplicationContext]]).

## Metadata phase vs instance phase

Container extension chapter: the two SPIs **look similar**; the **major** difference is the target. BFPP = configuration metadata **before** the container instantiates beans **other than** factory post-processors themselves. BPP = the **objects** created from that metadata ([[What is Spring BeanDefinition]]).

```d2
direction: down
defs: "BeanDefinitions loaded" {
  width: 220
  height: 36
  style.fill: "#e3f2fd"
}
bfpp: "BeanFactoryPostProcessor\npostProcessBeanFactory" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
new: "instantiate + inject" {
  width: 200
  height: 36
  style.fill: "#f3e5f5"
}
bpp: "BeanPostProcessor\nbefore-init → init → after-init / proxy" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}

defs -> bfpp -> new -> bpp
```

**Fig. 1.** `BeanDefinitionRegistryPostProcessor` (extends BFPP) can **add** definitions even earlier ([[What is BeanDefinitionRegistryPostProcessor]]).

| | **`BeanFactoryPostProcessor`** | **`BeanPostProcessor`** |
| --- | --- | --- |
| When | Definitions loaded; **no** app instances | **After** construct + populate |
| Method | `postProcessBeanFactory` (void) | Two methods; **return** instance or wrapper |
| Typical | Placeholders, property override, custom editors | `@Autowired`, `@PostConstruct`, AOP wrap |
| Built-in | `PropertySourcesPlaceholderConfigurer` ([[What is PropertySourcesPlaceholderConfigurer]]) | `AutowiredAnnotationBeanPostProcessor`, auto-proxy creators |
| `@Bean` | **`static`** (avoid initializing the `@Configuration` class) | **`static`**, ideally **no** deps |

Both are **per-container** (parent/child contexts do not share processors). Auto-detected processors honor **`PriorityOrdered` then `Ordered`**; **`@Order` is ignored** on **both**. Programmatic registration uses **registration order** and ignores `Ordered`. Lazy-init on these types is **ignored** — they still instantiate eagerly (otherwise they might never run).

```java
public class ScopeTweakingPostProcessor implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory factory) {
        factory.getBeanDefinition("audit").setScope(BeanDefinition.SCOPE_PROTOTYPE);
    }
}

public class TracingBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        return bean; // or a proxy
    }
}
```

**Listing 1.** Conceptual. Left: change the **definition**. Right: touch the **object** (after init if wrapping).

> [!warning] `getBean` inside a BFPP is a lifecycle bug
> It can create a singleton **before** BPPs are registered, so that bean **misses** `@Autowired` / AOP. Need an instance? That is a **BPP** (or inject the collaborator later).

> [!warning] Dump’s one-liners omit `@Bean static`
> A non-static `@Bean` that returns a BFPP (or BPP) **eagerly** initializes the configuration class; `@Autowired` / `@Value` / `@PostConstruct` on that class can fail. Mark the factory method **`static`**.

> [!tip] Interview answer
> BeanFactoryPostProcessor changes BeanDefinitions before any normal bean exists — PropertySourcesPlaceholderConfigurer is the example. BeanPostProcessor runs on each created instance, before and after init, and that is where Spring wraps proxies. I do not call getBean from a factory post-processor, and I do not confuse this pair with FactoryBean.
