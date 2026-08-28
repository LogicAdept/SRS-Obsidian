<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `@EnableLoadTimeWeaving` annotation?

> [!abstract] Short answer
> **`@EnableLoadTimeWeaving`** (Spring 3.1+) is the Java equivalent of **`<context:load-time-weaver/>`**. On a **`@Configuration`** class it registers a **`LoadTimeWeaver` bean named `loadTimeWeaver`**. It does **not** turn off Spring AOP proxies and it does **not** attach a JVM agent by itself.

## Bean, not a weaving mode switch

Place it on `@Configuration`. The default weaver is **`DefaultContextLoadTimeWeaver`**. Beans that implement **`LoadTimeWeaverAware`** (JPA factory beans, `AspectJWeavingEnabler`) receive it. To supply your own weaver, implement **`LoadTimeWeavingConfigurer`** and return it from `getLoadTimeWeaver()`.

```java
@Configuration
@EnableLoadTimeWeaving
public class AppConfig {
}
```

**Listing 1.** Same infrastructure as `<beans><context:load-time-weaver/></beans>`. Use an **`ApplicationContext`**, not a raw `BeanFactory`.

`aspectjWeaving` defaults to **`AUTODETECT`**. Attribute versus XML:

| Annotation | XML | Effect |
| --- | --- | --- |
| `ENABLED` | `on` | Register AspectJ’s `ClassFileTransformer` |
| `DISABLED` | `off` | Do not AspectJ-weave, even if `aop.xml` exists |
| `AUTODETECT` (default) | `autodetect` | AspectJ LTW **on** if at least one **`META-INF/aop.xml`** is on the classpath |

```java
@Configuration
@EnableLoadTimeWeaving(aspectjWeaving = EnableLoadTimeWeaving.AspectJWeaving.ENABLED)
public class AspectJLtwConfig {
}
```

**Listing 2.** Forces the AspectJ transformer. You still need **`aspectjweaver`**, compiled aspects, [[What is aop.xml for load-time weaving]], and an instrumentable loader or agent — [[What is a load-time weaver in Spring]], [[Why do you need a Java agent for load-time weaving]].

```d2
direction: right
ann: "@EnableLoadTimeWeaving" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
bean: "loadTimeWeaver" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
aj: "aspectjWeaving" {
  width: 160
  height: 45
  style.fill: "#e8f5e9"
}
auto: "AUTODETECT\nif aop.xml" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
on: "ENABLED" {
  width: 120
  height: 40
  style.fill: "#c8e6c9"
}
off: "DISABLED" {
  width: 120
  height: 40
  style.fill: "#ffcdd2"
}

ann -> bean
ann -> aj
aj -> auto
aj -> on
aj -> off
```

**Fig. 1.** The annotation always publishes the weaver bean. Only `aspectjWeaving` decides whether AspectJ’s adapter is added.

Contrast with **`@EnableAspectJAutoProxy`**: that one is `<aop:aspectj-autoproxy/>` — **proxies**, AspectJ runtime **not** involved. You can enable both; they are not substitutes. See [[What is the difference between EnableLoadTimeWeaving and EnableAspectJAutoProxy]].

> [!warning]ENABLED is not an agent and not aop.xml
> **`aspectjWeaving = ENABLED`** only registers the AspectJ transformer through `LoadTimeWeaver.addTransformer`. Generic Java / standalone Boot still start with **`-javaagent:…/spring-instrument.jar`** unless the container `ClassLoader` already supports transformers (Tomcat, WildFly). `aop.xml` still names aspects and `include` packages. Putting the annotation on `@SpringBootApplication` is legal (`@SpringBootApplication` is `@Configuration`) but does **not** weave every class already loaded or outside `weaver` includes.

> [!warning]XML spring-configured is not implied
> With XML, `aspectj-weaving="on"` **implicitly** enables **`<context:spring-configured>`** (`@Configurable`). **`@EnableLoadTimeWeaving(aspectjWeaving = ENABLED)` does not.** Add **`@EnableSpringConfigured`** from `spring-aspects` yourself.

> [!tip] Interview answer
> **`@EnableLoadTimeWeaving` registers Spring’s `loadTimeWeaver` bean, the Java form of `<context:load-time-weaver/>`.** Default `AUTODETECT` turns on AspectJ LTW only when `META-INF/aop.xml` is present; `ENABLED` / `DISABLED` override that. It is not `@EnableAspectJAutoProxy`, it does not install `spring-instrument`, and unlike the XML `on` flag it does not quietly enable `@Configurable` support.
