<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What is the default Spring bean scope?

> [!abstract] Short answer
> **`singleton`.** One shared instance **per bean definition per IoC container**, stored in the singleton cache; later `getBean` / injection of that **id** returns the **same** object ([[What happens when you request the same singleton bean twice from ApplicationContext]]). The scopes table marks it **(Default)**. Omitting `scope` on XML `<bean>`, omitting `@Scope` on `@Component` / `@Bean`, and `@Scope`’s empty `scopeName` (implies `ConfigurableBeanFactory.SCOPE_SINGLETON`) all mean singleton. It is **not** the GoF ClassLoader singleton ([[How does a Spring singleton differ from the Gang of Four Singleton pattern]]). The other five built-in scopes are opt-in ([[What are Spring bean scopes]]).

## Default recipe: one cached instance

Bean Scopes: you choose lifetime in **metadata**, not in the Java class. If you write nothing, the recipe is **singleton**. XML `scope="singleton"` is **redundant**. `ApplicationContext` then **eagerly pre-instantiates** those singletons at `refresh()` unless `@Lazy` / `lazy-init` ([[How do you create a singleton Spring bean at application startup]]). Eager startup is a **separate** default from the scope name.

```xml
<bean id="accountService" class="example.DefaultAccountService"/>
<bean id="alsoSingleton" class="example.DefaultAccountService" scope="singleton"/>
```

**Listing 1.** Conceptual. Both definitions are singleton. Two **ids** of the same class are **two** cached objects.

```java
@Component
class AccountService { }

@Bean
AccountService accountService() { return new AccountService(); }
```

**Listing 2.** Conceptual. No `@Scope` → singleton. Full `@Configuration` intercepts `@Bean` calls so you still get **one** instance despite two Java `new`s.

JSR-330 `@Named` / `@Inject` types in a Spring container are **still singleton**. The JSR-330 spec’s default is closer to Spring **prototype**; Spring **does not** follow that, so `@Singleton` is documentary unless you add `@Scope("prototype")`.

```d2
direction: down
def: "BeanDefinition\n(no scope / singleton)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
cache: "one instance in singleton cache" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
hits: "every getBean / inject of that id" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}

def -> cache
cache -> hits
```

**Fig. 1.** Default scope is **how many** objects. Default **eager** creation is **when** the first one is built.

Prototype, `request`, `session`, `application`, and `websocket` require an explicit `@Scope` / `scope="…"` (web scopes also need a web-aware context). Injecting a shorter-lived bean into this default singleton still **captures one** instance unless you use `ObjectProvider`, `@Lookup`, or a scoped proxy ([[How does a prototype Spring bean behave when injected into a singleton]]).

> [!warning] Dump mixed in Java `default` interface methods
> Interface `default` methods (Java 8 `Collection.stream()`) are **not** bean scope. The Spring default is the **`singleton`** scope identifier.

> [!warning] JSR-330 `@Singleton` is not what makes it singleton
> In Spring the bean is singleton **anyway**. Relying on jakarta.inject `@Singleton` to “turn on” singleton, or expecting spec-like prototype without `@Scope`, is the usual interview trap.

> [!tip] Interview answer
> Default Spring bean scope is singleton: one instance per definition per container, cached, returned on every lookup of that name. I do not set scope="singleton" unless I am being explicit. It is not a GoF singleton, not thread-safe by itself, and ApplicationContext also eagerly creates those singletons at startup unless they are lazy. JSR-330 beans in Spring are singleton too.
