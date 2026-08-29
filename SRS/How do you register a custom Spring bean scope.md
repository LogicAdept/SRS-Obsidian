<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# How do you register a custom Spring bean scope?

> [!abstract] Short answer
> Implement `org.springframework.beans.factory.config.Scope`, then register it **by name** with `ConfigurableBeanFactory.registerScope(name, scope)` or a `CustomScopeConfigurer` (`BeanFactoryPostProcessor`). Beans then use that name (`scope="thread"`, `@Scope("thread")`). You cannot replace the built-in `singleton` and `prototype` scopes. `SimpleThreadScope` ships with Spring but is **not** registered until you do this.

## Implement `Scope`, then register the name

The container’s built-in table is `singleton` (default), `prototype`, and — only on a web-aware `ApplicationContext` — `request`, `session`, `application`, and `websocket`. Constants: `ConfigurableBeanFactory.SCOPE_SINGLETON` / `SCOPE_PROTOTYPE`; `WebApplicationContext.SCOPE_REQUEST` / `SCOPE_SESSION` / `SCOPE_APPLICATION`. A **thread** scope exists as `SimpleThreadScope` but stays unused until registered. See [[What are Spring bean scopes]].

`Scope` is a storage SPI. **`get(name, ObjectFactory)`** is the only required method: return the object for this conversation, or call the factory and store it. `remove`, `registerDestructionCallback`, `resolveContextualObject`, and `getConversationId` are optional (`resolveContextualObject` / `getConversationId` default to `null` since Framework **7.0**). Implementations must be **thread-safe**. `get` throws `IllegalStateException` if the underlying scope is not active.

```d2
direction: down
impl: "1. Implement Scope\nget + optional remove/callbacks" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
reg: "2. registerScope or\nCustomScopeConfigurer" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
use: "3. scope=\"name\" / @Scope(\"name\")\n(+ scoped-proxy if injected wide)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

impl -> reg -> use
```

**Fig. 1.** Registration only publishes a name. Unknown names fail at bean creation (`IllegalStateException`), the same way `request`/`session` fail on a non-web `ClassPathXmlApplicationContext`.

```java
Scope threadScope = new SimpleThreadScope();
beanFactory.registerScope("thread", threadScope);
```

**Listing 1.** Conceptual. `registerScope` lives on `ConfigurableBeanFactory` (reachable from most `ApplicationContext` implementations). The name is whatever you pass, conventionally `"thread"` for `SimpleThreadScope`.

Declarative equivalent: a `CustomScopeConfigurer` bean whose `scopes` map keys are names and values are `Scope` instances or class names (`addScope` since **4.1.1**). It runs in `postProcessBeanFactory` — definitions loaded, **no beans instantiated yet** — which is the safe window.

```xml
<bean class="org.springframework.beans.factory.config.CustomScopeConfigurer">
    <property name="scopes">
        <map>
            <entry key="thread">
                <bean class="org.springframework.context.support.SimpleThreadScope"/>
            </entry>
        </map>
    </property>
</bean>
<bean id="thing2" class="x.y.Thing2" scope="thread">
    <aop:scoped-proxy/>
</bean>
```

**Listing 2.** Conceptual XML. Java config: a **`static` `@Bean`** `CustomScopeConfigurer` (it is a `BeanFactoryPostProcessor`; those types must not rely on `@Autowired` on the configuration instance). Then `@Scope("thread")` on the component.

You **may** redefine an existing custom/web scope; that is called out as bad practice. You **cannot** override `singleton` or `prototype`.

## After it is registered

A singleton that depends on a shorter-lived custom-scoped bean needs a **scoped proxy** (`<aop:scoped-proxy/>` or `@Scope(..., proxyMode = …)`), `ObjectFactory` / `ObjectProvider`, or lookup — the same rule as `request`/`session` ([[What is ObjectProvider and a scoped proxy in Spring]]). On a `FactoryBean`, the proxy scopes the **factory**, not `getObject()`.

> [!warning] `SimpleThreadScope` does not destroy
> It does not clean up stored objects. Destruction callbacks are not a reliable lifecycle. In a web app, prefer `request` / `RequestScope`, which implement full scoped-attribute destruction.

> [!warning] `globalSession` is not a current built-in
> Older lists include `WebApplicationContext.SCOPE_GLOBAL_SESSION` (`globalSession`) for Portlet. Framework **5** dropped Portlet MVC. Current `WebApplicationContext` exposes `SCOPE_REQUEST`, `SCOPE_SESSION`, and `SCOPE_APPLICATION` only. Details: [[What is global-session bean scope in Spring]].

> [!tip] Interview answer
> Implement Scope — get is the required method — then register the name with ConfigurableBeanFactory.registerScope or CustomScopeConfigurer. Put that name on the bean definition. Singleton and prototype cannot be replaced. Thread scope is SimpleThreadScope and is off until you register it; inject it into a singleton through a scoped proxy.
