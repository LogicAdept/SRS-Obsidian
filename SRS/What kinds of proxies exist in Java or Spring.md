<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Language/Reflection #SRS

# What kinds of proxies exist in Java or Spring?

> [!abstract] Short answer
> In the JDK, **`java.lang.reflect.Proxy`** builds a **runtime class that implements interfaces** and dispatches to an **`InvocationHandler`**. Spring AOP uses that **JDK dynamic proxy** when the target has interfaces, and otherwise (or when forced) a **CGLIB subclass** of the target class. Both are **runtime** proxies; they are not AspectJ bytecode weaving.

## JDK dynamic proxy

Java SE `Proxy`: `Proxy.newProxyInstance(loader, interfaces, handler)` returns an object that **acts like** those interfaces. The generated class is **final**, extends `Proxy`, and implements **exactly** the listed interfaces. Calls go to `InvocationHandler.invoke`. You **cannot** proxy a class that has no interface this way.

## Spring’s two AOP mechanisms

Spring *Proxying Mechanisms*:

| Kind | When | What is intercepted |
| --- | --- | --- |
| **JDK dynamic proxy** | Target implements ≥1 interface (Framework default) | Methods on those **interfaces** |
| **CGLIB** | No interfaces, or `proxyTargetClass=true` / Boot class-proxy default | Overridable methods on a **generated subclass** |

CGLIB is repackaged in `spring-core`. Tradeoffs (final, private, self-invocation): [[What are Spring AOP proxy limitations]], [[What is an AOP proxy in Spring]].

```d2
direction: down
jdk: "JDK Proxy\ninterfaces + InvocationHandler" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
cglib: "CGLIB subclass\nextends target class" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
target: "Target bean" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}

jdk -> target
cglib -> target
```

**Fig. 1.** Two runtime wrappers; AspectJ weaving is a third, non-proxy path. Per-bean override as of Spring 7: `@Proxyable(INTERFACES)` / `TARGET_CLASS`.

> [!warning] JDK proxy `instanceof` the class is false
> The object is `instanceof` the **interfaces**, not the concrete class. Casting to the implementation type fails.

> [!warning] “Proxy” in interviews is not Hibernate lazy loading by default
> Same word, different libraries. This cue is **JDK `Proxy` + Spring AOP**. JPA lazy proxies are a separate mechanism.

> [!tip] Interview answer
> **Java’s built-in proxy is `java.lang.reflect.Proxy` — interface-only, `InvocationHandler`.** Spring AOP uses that, or CGLIB to subclass the target when there is no interface or you force class proxies. Callers get the proxy from the container; neither kind sees `this` calls inside the target.
