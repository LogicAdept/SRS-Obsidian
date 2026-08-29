<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS

# What `Aware` interfaces does Spring invoke during bean initialization?

> [!abstract] Short answer
> After properties are set and **before** `InitializingBean.afterPropertiesSet()` / `init-method`, the container calls `Aware` setters on beans that implement them. The usual factory ones are `BeanNameAware` and `BeanFactoryAware`. An `ApplicationContext` also injects `ApplicationContextAware`, and prefers the narrower `ResourceLoaderAware`, `ApplicationEventPublisherAware`, and `MessageSourceAware` when that is all you need. These APIs **couple** the class to Spring; inject collaborators (or even `ApplicationContext`) instead when you can.

## Callbacks after properties, before init

`Aware` means “give this bean a container infrastructure object.” The name of the interface is the dependency. Invocation is **after** normal property population and **before** an init callback such as `afterPropertiesSet()` or a custom init-method ([[In what order do PostConstruct InitializingBean and init-method run]], [[How do you call a method after a Spring bean is initialized]]).

Factory-level (any `BeanFactory` that honors the contract):

- `BeanNameAware.setBeanName` — the **actual** id in the factory (inner beans may have a `#…` uniqueness suffix).
- `BeanFactoryAware.setBeanFactory` — the owning factory; you may call it immediately (lookup). Injection of collaborators is still preferred over lookup.
- `BeanClassLoaderAware` — the class loader used for bean classes.

`ApplicationContext` additionally detects context-oriented interfaces. `ApplicationContextAware.setApplicationContext` runs in that same window, and **after** `ResourceLoaderAware`, `ApplicationEventPublisherAware`, and `MessageSourceAware` when those also apply. Prefer those three over grabbing the whole context just for resources, events, or i18n ([[How does ApplicationContext publish events]], [[What is MessageSource in Spring]]). File resources can be a `Resource` property instead of `ResourceLoaderAware`.

The reference lists these as the **most important** `Aware` types (not every `Aware` in the framework):

| Interface | Injected |
| --- | --- |
| `BeanNameAware` | Bean id in the factory |
| `BeanFactoryAware` | Owning `BeanFactory` |
| `BeanClassLoaderAware` | Bean class loader |
| `ApplicationContextAware` | The creating `ApplicationContext` |
| `ApplicationEventPublisherAware` | Context as event publisher |
| `MessageSourceAware` | i18n `MessageSource` |
| `ResourceLoaderAware` | Resource loading |
| `LoadTimeWeaverAware` | Load-time weaver |
| `NotificationPublisherAware` | JMX notification publisher |
| `ServletConfigAware` / `ServletContextAware` | Servlet environment — **web-aware** context only |

You can also **autowire** `ApplicationContext` (constructor / `byType` / `@Autowired`) instead of implementing `ApplicationContextAware`.

```java
public class LookupBean implements BeanNameAware, BeanFactoryAware, ApplicationContextAware {

    private String beanName;
    private BeanFactory factory;

    @Override
    public void setBeanName(String name) {
        this.beanName = name;
    }

    @Override
    public void setBeanFactory(BeanFactory beanFactory) {
        this.factory = beanFactory;
    }

    @Override
    public void setApplicationContext(ApplicationContext context) {
        // after ResourceLoaderAware / ApplicationEventPublisherAware / MessageSourceAware
    }
}
```

**Listing 1.** Conceptual. Three common callbacks; `setApplicationContext` is last among the context-specific ones named in that Javadoc.

```d2
direction: down
props: "Populate properties" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
aware: "Aware setters\n(BeanName, BeanFactory, context…)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
init: "afterPropertiesSet\ninit-method" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

props -> aware -> init
```

**Fig. 1.** Official slot: after properties, before `InitializingBean` / `init-method`. Use that window for receiving infrastructure, not for finishing the whole singleton graph.

Spring recommends `Aware` for **infrastructure** beans that truly need programmatic container access. Application code should take collaborators as constructor arguments. Implementing `ApplicationContextAware` only to `getBean` is documented as worse than bean references — it is a service locator next to IoC ([[What is the difference between BeanFactory and ApplicationContext]]).

> [!warning] Lookup during Aware is still mid-creation
> `setBeanFactory` may call the factory at once, but other singletons may not exist yet. Reaching out to collaborators here has the same deadlock / incomplete-graph risk as heavy work in `@PostConstruct` (still inside the singleton creation lock). Inject dependencies instead.

> [!warning] `ApplicationContextAware` is the blunt tool
> If you only need to publish events, load a file, or resolve a message, implement the **specific** `Aware` (or autowire `ApplicationEventPublisher` / `Resource` / `MessageSource`). `ServletContextAware` does nothing useful in a non-web `ApplicationContext`.

> [!tip] Interview answer
> After injection Spring calls Aware interfaces before afterPropertiesSet and init-method. BeanNameAware and BeanFactoryAware are the factory ones; an ApplicationContext also calls ApplicationContextAware, after ResourceLoaderAware, ApplicationEventPublisherAware, and MessageSourceAware if those are present. They couple you to Spring, so prefer constructor injection, including autowiring ApplicationContext when you really need it. ServletContextAware is web-only.
