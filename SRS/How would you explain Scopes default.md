<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# How would you explain Scopes default?

> [!abstract] Short answer
> The **default** Spring bean scope is **`singleton`**: one shared instance **per bean definition per IoC container**, kept in the singleton cache. Omitting `scope` on XML `<bean>` and omitting `@Scope` on `@Component` / `@Bean` both mean singleton. `scope="singleton"` is redundant. That default is **not** “one instance in the JVM” and **not** the same fact as **eager** singleton pre-instantiation at `refresh()`.

## Default means singleton, per container

The scopes table marks **singleton** as **(Default)**. The container creates **exactly one** object for that definition, caches it, and returns it for later `getBean` and injection of that **id** ([[What is the default Spring bean scope]], [[Which scopes]]).

```xml
<bean id="accountService" class="example.DefaultAccountService"/>
<bean id="alsoDefault" class="example.DefaultAccountService" scope="singleton"/>
```

**Listing 1.** Conceptual. Both are singleton. Two **ids** → two cached instances of the same class.

```java
@Component
class AccountService { }

@Bean
AccountService accountService() {
	return new AccountService();
}
```

**Listing 2.** Conceptual. No `@Scope` → `ConfigurableBeanFactory.SCOPE_SINGLETON`.

```d2
direction: right
def: "Bean definition\n(no scope set)" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
cache: "Singleton cache\none instance" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
def -> cache: "default"
```

**Fig. 1.** Unspecified scope is singleton, not prototype.

The other five built-in scopes are **opt-in**. JSR-330 `@Named` types in Spring are **still singleton**; Spring does not adopt the JSR-330 “prototype-like” default ([[What are Spring bean scopes]]).

> [!warning] Default scope ≠ eager creation
> `ApplicationContext` **pre-instantiates** non-lazy singletons at startup. That is a **separate** default. `@Lazy` / `lazy-init` delays creation; the bean is **still singleton** when it appears.

> [!tip] Interview answer
> Default scope is singleton: one instance per bean definition per container, not per ClassLoader. You do not write scope="singleton". Prototype and the four web scopes you choose explicitly. Eager startup of singletons is a different knob from the scope name.
