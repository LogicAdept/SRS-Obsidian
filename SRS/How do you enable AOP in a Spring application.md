<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# How do you enable AOP in a Spring application?

> [!abstract] Short answer
> Turn on **`@AspectJ` auto-proxying**: **`@EnableAspectJAutoProxy`** on a `@Configuration` class, or XML **`<aop:aspectj-autoproxy/>`**. Put **`aspectjweaver`** on the classpath. Register **`@Aspect` beans**. In **Spring Boot**, if AspectJ is on the classpath (typically **`spring-boot-starter-aop`**), auto-config does this and you usually **omit** the annotation.

## Framework vs Boot

Spring Framework *Enabling @AspectJ Support*: enable Spring AOP based on `@Aspect` classes and **auto-proxy** advised beans. That is still **proxy-based Spring AOP**, not compile-time AspectJ weaving.

```java
@Configuration
@EnableAspectJAutoProxy
public class ApplicationConfiguration {
}
```

**Listing 1.** Programmatic enablement from Spring Framework reference. XML equivalent: `<aop:aspectj-autoproxy/>`.

You still need:

1. **`org.aspectj:aspectjweaver`** (1.9+) on the classpath  
2. Aspect classes as **beans** (`@Component` + scan or `@Bean`) — [[What is the Aspect annotation used for]]

Spring Boot *Aspect-Oriented Programming*: if **AspectJ is on the classpath**, auto-config enables AspectJ auto-proxy so **`@EnableAspectJAutoProxy` is not required**. Default proxies are **CGLIB** (`spring.aop.proxy-target-class=true`); set `false` for JDK interface proxies. Disable with `spring.aop.auto=false`. Boot-focused cue: [[Can you use Spring AOP with Spring Boot]].

```d2
direction: down
enable: "@EnableAspectJAutoProxy\nor Boot AopAutoConfiguration" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
beans: "@Aspect beans +\nadvised @Service beans" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
proxy: "Runtime AOP proxies" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

enable -> beans -> proxy
```

**Fig. 1.** Enablement only switches auto-proxy on; aspects and targets must still be beans in **that** context. Annotation details: [[What is the EnableAspectJAutoProxy annotation]].

> [!warning] Local `ApplicationContext` only
> `@EnableAspectJAutoProxy` applies to **its own** context. A child `DispatcherServlet` context does not inherit it — redeclare if controllers there must be advised.

> [!warning] Annotation without weaver / without aspect beans
> Missing `aspectjweaver` breaks `@AspectJ` support. An `@Aspect` class that is not a bean is ignored.

> [!tip] Interview answer
> **Enable with `@EnableAspectJAutoProxy` (or `<aop:aspectj-autoproxy/>`) and register `@Aspect` beans; keep `aspectjweaver` on the classpath.** Boot’s AOP starter auto-enables this. It still creates Spring proxies, not full AspectJ weaving.
