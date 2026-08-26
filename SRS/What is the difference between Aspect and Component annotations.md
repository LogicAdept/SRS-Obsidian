<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the difference between Aspect and Component annotations?

> [!abstract] Short answer
> **`@Component` registers a Spring bean** (stereotype / component-scan). **`@Aspect` marks that bean’s class as an aspect** (pointcuts + advice). They solve different jobs: **`@Aspect` is not a stereotype** and does **not** create a bean. Typical production code uses **both**. `@Component` alone is just a bean — no AOP unless something else advises it.

## Two annotations, two pipelines

Spring *Declaring an Aspect*: `@Aspect` beans are detected for auto-proxy configuration. **Autodetecting through component scanning** still needs **`@Component`** (or another qualifying stereotype). `@Aspect` by itself is **not sufficient** for classpath scan.

| | **`@Component`** | **`@Aspect`** |
| --- | --- | --- |
| Role | IoC: make a bean | AOP: this bean is an aspect |
| Component-scan | Yes | **No** (not a stereotype) |
| Without the other | Bean with no aspect metadata | Aspect class **ignored** if not a bean |
| Auto-proxy target | May be advised by aspects | **Excluded** from being advised |

```java
@Aspect
@Component
public class LoggingAspect { }

@Component
public class OrderService { }  // not an aspect; may be proxied if advised
```

**Listing 1.** Scan picks up both; only `LoggingAspect` contributes advice. See [[What is the Aspect annotation used for]], [[What is an Aspect in Spring AOP]].

Equivalent without scan: `@Bean` factory method returning an `@Aspect` instance plus `@EnableAspectJAutoProxy`.

```d2
direction: down
scan: "Component scan" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
comp: "@Component → bean" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
asp: "@Aspect → AOP config" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}

scan -> comp -> asp
```

**Fig. 1.** Scan uses `@Component`; AOP infrastructure then reads `@Aspect` on that bean.

> [!warning] Only `@Aspect` → nothing happens
> No bean, no auto-proxy, no advice. Interview trap: treating `@Aspect` like `@Service`.

> [!warning] Only `@Component` → not an aspect
> The class is a normal bean. Advice lives elsewhere. Do not expect `@Before` methods to run without `@Aspect` (and enablement).

> [!tip] Interview answer
> **`@Component` is “this is a bean.” `@Aspect` is “this bean is an aspect.”** You almost always pair them (or use `@Bean`). `@Aspect` does not replace component scanning, and Spring will not advise other aspects.
