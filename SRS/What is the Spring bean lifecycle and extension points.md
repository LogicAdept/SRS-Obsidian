<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS

# What is the Spring bean lifecycle and extension points?

> [!abstract] Short answer
> **Container first, then each bean.** `refresh()` loads **`BeanDefinition`s**, runs **`BeanDefinitionRegistryPostProcessor`** then **`BeanFactoryPostProcessor`** (edit recipes — e.g. `${…}`), registers **`BeanPostProcessor`s**, then **creates non-lazy singletons**. For each bean: **instantiate** (constructor / factory / `FactoryBean.getObject()`) → **inject** → **`Aware`** → **`postProcessBeforeInitialization`** (`@PostConstruct` lives here) → **`InitializingBean` / `init-method`** → **`postProcessAfterInitialization`** (**AOP proxy**) ([[In what order does Spring initialize a bean and its dependencies]]). Shutdown (managed scopes): **`@PreDestroy`** → **`DisposableBean`** → **`destroy-method`**. Extension points are those processor SPIs, not a separate “FactoryBean phase.”

## Two clocks: `refresh()` and `createBean`

Dump’s numbered “IoC start” mixes **context bootstrap** with **one bean’s** callbacks. Official split:

**`refresh()` (factory-level)** — [[How does Spring work under the hood]]

1. Parse metadata → `BeanDefinition` registry ([[What is Spring BeanDefinition]]).
2. **`BeanDefinitionRegistryPostProcessor`** — may **add** definitions ([[What is BeanDefinitionRegistryPostProcessor]]).
3. **`BeanFactoryPostProcessor`** — change metadata; **no** ordinary instances yet (`PropertySourcesPlaceholderConfigurer`). **Do not `getBean` here** ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]]).
4. Instantiate **BPP** beans, then **`preInstantiateSingletons`**.
5. After all singletons: `SmartInitializingSingleton`, then **`Lifecycle` / `SmartLifecycle`**.

**`FactoryBean`** is a **bean type** that manufactures another object during **instantiation**, not a step between BFPP and `createBean` ([[What is the difference between BeanFactory and FactoryBean]]).

**One instance (`BeanFactory` javadoc order)** — populate first, then:

```d2
direction: down
new: "instantiate + inject" {
  width: 220
  height: 36
  style.fill: "#e3f2fd"
}
aware: "Aware callbacks" {
  width: 200
  height: 36
  style.fill: "#fff3e0"
}
before: "BPP before-init\n(@PostConstruct)" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}
init: "afterPropertiesSet\n+ init-method" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
after: "BPP after-init\n(AOP proxy)" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}

new -> aware -> before -> init -> after
```

**Fig. 1.** Init callbacks run on the **raw** target. `@Transactional` / AspectJ auto-proxy wrap in **after-init** ([[What is Spring BeanPostProcessor]], [[What is an AOP proxy in Spring]]).

`@PostConstruct` → `afterPropertiesSet` → `init-method` when names differ ([[In what order do PostConstruct InitializingBean and init-method run]]). Destroy uses the **same** sequence, not reverse: `@PreDestroy` (destruction BPP) → `DisposableBean.destroy` → `destroy-method` ([[What destroy callbacks does Spring invoke when a bean is destroyed]]). Prototypes get **init**, not container **destroy**.

```java
@Component
public class BillingService implements InitializingBean, DisposableBean {
	@PostConstruct
	void postConstruct() { /* BPP before-init — no AOP yet */ }
	@Override
	public void afterPropertiesSet() { /* after @PostConstruct */ }
	@Override
	public void destroy() { /* after @PreDestroy */ }
}
```

**Listing 1.** Conceptual. Prefer POJO `init-method` / `@PreDestroy` over Spring interfaces when you can.

Further SPIs: **`InstantiationAwareBeanPostProcessor`** (can skip construction; property injection), **`MergedBeanDefinitionPostProcessor`**, **`DestructionAwareBeanPostProcessor`**. `ApplicationContext` **auto-detects** BFPP/BPP; a raw `BeanFactory` does not.

> [!warning] `@PostConstruct` is not “after the proxy”
> The advised bean is wrapped **later**. Calling `this.txMethod()` from `@PostConstruct` **skips** interceptors. Inject a `@Lazy` self-reference or split types if you need the proxy ([[How do you fix a circular dependency caused by self-injection in Spring]]).

> [!warning] Dump’s “create custom FactoryBean” step
> `FactoryBean` instances are **beans**. Their **`getObject()`** product is what `getBean("id")` returns. They are not a fourth bootstrap phase between placeholders and `new`.

> [!tip] Interview answer
> Refresh loads definitions, BeanFactoryPostProcessors edit them, then each singleton is instantiated, injected, Aware, PostConstruct, afterPropertiesSet, init-method, then BeanPostProcessor after-init where AOP proxies appear. Destroy is PreDestroy, DisposableBean, destroy-method. I name BeanFactoryPostProcessor versus BeanPostProcessor as the two main extension points: recipes versus instances.
