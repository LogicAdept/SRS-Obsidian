<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS

# Which well-known types can Autowired inject without a matching bean?

> [!abstract] Short answer
> Spring resolves **`@Autowired`** (and JSR-330 **`@Inject`**) on **well-known resolvable dependencies** to the **container itself** — no collaborator **`@Bean`** required. The framework docs list **`BeanFactory`**, **`ApplicationContext`**, **`Environment`**, **`ResourceLoader`**, **`ApplicationEventPublisher`**, and **`MessageSource`**, plus **extended sub-interfaces** such as **`ConfigurableApplicationContext`** and **`ResourcePatternResolver`**.

## Built-in container dependencies

Ordinary **`@Autowired`** looks up a **bean definition** of the requested type. For the types above, Spring treats the **`ApplicationContext` / `BeanFactory`** as the provider: they are **always available** when the container is up.

```java
@Service
public class OrderNotifier {

    private final ApplicationEventPublisher events;
    private final MessageSource messages;

    public OrderNotifier(ApplicationEventPublisher events, MessageSource messages) {
        this.events = events;
        this.messages = messages;
    }
}
```

**Listing 1.** Constructor injection of infrastructure interfaces — no `@Bean` of those types needed.

| Type | Typical use |
|---|---|
| **`BeanFactory`** | Low-level bean lookup / metadata |
| **`ApplicationContext`** | Full container API (beans, events, i18n, resources) |
| **`Environment`** | **`${…}`** property access, profiles, **`@Conditional`** context |
| **`ResourceLoader`** | Load **`classpath:`** / **`file:`** resources |
| **`ApplicationEventPublisher`** | Publish domain events without depending on the whole context |
| **`MessageSource`** | Resolve localized messages (often auto-configured in Boot) |

This mirrors the **Aware** callback family (**`BeanFactoryAware`**, **`ApplicationContextAware`**, **`MessageSourceAware`**, …) but keeps injection **declarative** via **`@Autowired`** instead of implementing `*Aware` interfaces. See [[What Aware interfaces does Spring invoke during bean initialization]].

```d2
direction: right
bean: "Your @Service bean" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
autowire: "@Autowired\nwell-known type" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
ctx: "ApplicationContext\n(resolves internally)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}

bean -> autowire -> ctx
```

**Fig. 1.** The container satisfies infrastructure-type injection points directly.

> [!warning] Prefer narrow types over full `ApplicationContext`
> Injecting **`ApplicationContext`** only to call **`getBean()`** is a **service-locator smell** — prefer constructor injection of the actual collaborator. **`ApplicationEventPublisher`** is the usual narrow choice for events; **`MessageSource`** for i18n ([[What is MessageSource in Spring]]). **`Environment`** beats pulling properties through the context when you only need configuration access.

> [!tip] Interview answer
> Spring autowires BeanFactory, ApplicationContext, Environment, ResourceLoader, ApplicationEventPublisher, and MessageSource without a declared bean — the container resolves them automatically, including extended interfaces. Same idea as Aware callbacks. Use ApplicationEventPublisher or specific collaborators instead of ApplicationContext.getBean() when you can.
