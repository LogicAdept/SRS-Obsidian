<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# What does `context:annotation-config` register?

> [!abstract] Short answer
> `<context:annotation-config/>` does **not** scan for `@Component`. It registers the **annotation processors** so existing bean definitions honor annotations: `ConfigurationClassPostProcessor` (`@Configuration` / `@Bean`), `AutowiredAnnotationBeanPostProcessor` (`@Autowired`, `@Value`, `@Inject`), `CommonAnnotationBeanPostProcessor` (`@Resource`, `@PostConstruct`, `@PreDestroy`), `PersistenceAnnotationBeanPostProcessor` (JPA), and `EventListenerMethodProcessor` (`@EventListener`). `AnnotationConfigApplicationContext` registers the same set. `<context:component-scan>` **includes** this behavior **and** scans packages.

## Processors, not a component scan

Spring drives annotation injection through `BeanPostProcessor` / `BeanFactoryPostProcessor` beans. You can declare them by class, but XML `<context:annotation-config/>` (and `AnnotationConfigUtils.registerAnnotationConfigProcessors`) installs the usual set. `AnnotationConfigApplicationContext` does that implicitly — you do not add the XML tag there.

What those processors do:

| Processor | Role |
| --- | --- |
| `ConfigurationClassPostProcessor` | Parse `@Configuration` / `@Bean` (and `@Import`, `@ComponentScan` on config classes) |
| `AutowiredAnnotationBeanPostProcessor` | `@Autowired`, `@Value`; also JSR-330 `@Inject` |
| `CommonAnnotationBeanPostProcessor` | `@Resource`, `@PostConstruct`, `@PreDestroy` |
| `PersistenceAnnotationBeanPostProcessor` | JPA persistence annotations |
| `EventListenerMethodProcessor` | `@EventListener` methods ([[How does ApplicationContext publish events]]) |

Older dumps add `RequiredAnnotationBeanPostProcessor` (`@Required`). That processor is **not** in the current registration list; `@Required` is a separate, retired story ([[What is the Required annotation in Spring]]).

`<context:component-scan base-package="…"/>` **implicitly enables** `annotation-config`. You almost never need both. Scan still needs the extra tag (or `@ComponentScan`) because `annotation-config` **only** processes annotations on beans **already** in that context — it does not discover `@Component` classes ([[What is the Spring ComponentScan annotation]], [[How do ComponentScan include and exclude filters work]]).

`component-scan` lets you turn those two post-processors off: `annotation-config="false"` skips registering `AutowiredAnnotationBeanPostProcessor` and `CommonAnnotationBeanPostProcessor` (for example if you supply your own). `CommonAnnotationBeanPostProcessor`’s Javadoc: remove or disable the default annotation-config registration before declaring a **custom** instance of that processor.

Processors apply only in the **same** `ApplicationContext` that defines the tag. `annotation-config` in a `DispatcherServlet` `WebApplicationContext` autowires **controllers** in that child, not services in the root context.

Annotation injection runs **before** XML `<property>` injection, so XML can override an annotated property in mixed configuration.

```xml
<beans>
    <context:annotation-config/>
    <bean class="example.MovieRecommender"/>
</beans>
```

**Listing 1.** Conceptual. `MovieRecommender` must already be a bean; `@Autowired` then works. No package is scanned.

```xml
<context:component-scan base-package="example"/>
```

**Listing 2.** Conceptual. Scan **plus** the same processors. Do not also add `annotation-config` unless you have a reason.

```d2
direction: down
xml: "context:annotation-config" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
cfg: "ConfigurationClassPostProcessor" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
autowired: "AutowiredAnnotationBeanPostProcessor" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
common: "CommonAnnotationBeanPostProcessor" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
jpa: "PersistenceAnnotationBeanPostProcessor" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
events: "EventListenerMethodProcessor" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}

xml -> cfg
xml -> autowired
xml -> common
xml -> jpa
xml -> events
```

**Fig. 1.** Annotation-config registers processors against **existing** bean definitions. Component-scan is what finds `@Component` types.

> [!warning] No scan, no new `@Component` beans
> `annotation-config` on an empty XML file does nothing useful. You still need `<bean>` entries, `component-scan`, or a Java `AnnotationConfigApplicationContext` with registered classes. Putting the tag only in the servlet child context will not `@Autowired` the root service layer.

> [!warning] Do not double-register a custom `CommonAnnotationBeanPostProcessor`
> If you declare your own, turn off the default (`component-scan` `annotation-config="false"` or drop `annotation-config`) as that class’s Javadoc requires. Do not expect a `RequiredAnnotationBeanPostProcessor` from current Spring.

> [!tip] Interview answer
> annotation-config registers the annotation post-processors so @Autowired, @Value, @Resource, @PostConstruct, @PreDestroy, @Configuration, and @EventListener work on beans you already defined. It does not scan the classpath. component-scan does the scan and already includes those processors, so you rarely use both. AnnotationConfigApplicationContext registers the same processors without XML.
