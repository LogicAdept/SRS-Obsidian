<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# How does Spring work under the hood?

> [!abstract] Short answer
> Spring is **not** a hidden application server. Under the hood is an **IoC container**: it reads **configuration metadata**, turns it into **`BeanDefinition`s**, then **`refresh()`** builds a **`BeanFactory`**, runs **`BeanFactoryPostProcessor`s** (edit blueprints), registers **`BeanPostProcessor`s**, and **creates singletons**. Each bean is **instantiated**, **populated** (dependency injection), then **initialized** (Aware callbacks, init methods, post-processors that may **wrap a proxy**). You write POJOs; the container **new**s and wires them ([[How would you explain dependency injection]], [[What is the Spring Framework]]). MVC, transactions, and Boot sit **on** that factory — they do not replace it.

## Metadata in, graph out

`ApplicationContext` **is** the IoC container in ordinary apps (`BeanFactory` is the root SPI; context adds events, messages, resources). It does not execute your business methods. It **instantiates, configures, and assembles** beans from XML, annotations, or `@Bean` methods. `AnnotationConfigApplicationContext(AppConfig.class)` constructs **and** `refresh()`es.

`refresh()` “loads or refreshes the persistent representation of the configuration.” On failure it **destroys** singletons already made so you never keep a half-started context ([[What is the difference between close and refresh on ApplicationContext]]).

```d2
Meta: "XML / @Configuration / @Component"
Defs: "BeanDefinition registry"
BFPP: "BeanFactoryPostProcessor\n(placeholders, conditions)"
BPP: "register BeanPostProcessor"
Create: "createBean: new → inject → init"
Cache: "singleton cache"
Meta -> Defs -> BFPP -> BPP -> Create -> Cache
Create -> Proxy: "BPP may return AOP proxy"
```

**Fig. 1.** `refresh()`: definitions first, instances last. Post-processors are the documented extension points — you do not subclass the context.

Official `AbstractApplicationContext` steps (names matter in interviews): `prepareRefresh` → `obtainFreshBeanFactory` → `prepareBeanFactory` → `invokeBeanFactoryPostProcessors` (**before** application singletons) → `registerBeanPostProcessors` (**before** those singletons) → message source / event multicaster → `onRefresh` → `registerListeners` → `finishBeanFactoryInitialization` (remaining **non-lazy singletons**) → `finishRefresh` (`LifecycleProcessor.onRefresh()`, `ContextRefreshedEvent`).

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
InvoiceService invoices = ctx.getBean(InvoiceService.class);
```

**Listing 1.** The constructor’s `refresh()` is the “under the hood” start. After it returns, eager singletons exist. `getBean` in a `@Service` is a locator — the DI chapter wants constructor injection instead.

## One bean’s lifecycle inside `createBean`

For a typical singleton:

1. **Instantiate** — constructor, factory method, or `FactoryBean.getObject()` (the factory is a **bean in** the container, not the container — [[What is the difference between BeanFactory and FactoryBean]]).
2. **Populate** — setter/field/`@Autowired` injection. `AutowiredAnnotationBeanPostProcessor` is how annotation injection is implemented.
3. **Initialize** — `BeanNameAware` / `BeanFactoryAware` / …, then `BeanPostProcessor.postProcessBeforeInitialization`, then `InitializingBean` / `@PostConstruct` / `init-method`, then `postProcessAfterInitialization`. AOP auto-proxying **is** a post-processor: it may **replace** the instance with a proxy. The object in the singleton cache is that **final** reference.

`BeanFactoryPostProcessor` runs on **definitions** (`PropertySourcesPlaceholderConfigurer` expands `${…}`) and must not `getBean` application types — that **pre-creates** beans and skips later post-processing. `BeanPostProcessor` runs on **instances**. Context **auto-registers** both when they are beans.

## Everything else is a client of this factory

Declarative `@Transactional` and security advice are **proxies** around those singletons (self-invocation on `this` skips them). `DispatcherServlet` is a servlet that asks a **web** `ApplicationContext` for handlers. Boot chooses an `ApplicationContext` subtype and auto-config `@Bean`s — still this `refresh()` pipeline.

> [!warning] Post-processor beans skip the usual AOP pass
> `BeanPostProcessor` instances (and beans they **directly** reference) are created in a **special early phase**. They are **not eligible for auto-proxying**. Wiring a random `@Service` into a custom post-processor can pull that service into the same early set. Log line: not eligible for auto-proxying.

> [!tip] Interview answer
> Spring under the hood is `refresh()` on an `ApplicationContext`: load `BeanDefinition`s, `BeanFactoryPostProcessor`s, `BeanPostProcessor`s, then instantiate–inject–initialize singletons (proxies last). The rest of the portfolio is modules and Boot conventions on that container.
