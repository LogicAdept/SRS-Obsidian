<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #SRS

# What is a load-time weaver in Spring?

> [!abstract] Short answer
> A **`LoadTimeWeaver`** is Spring’s SPI for attaching **`ClassFileTransformer`s** to a **`ClassLoader`** so classes can be **rewritten as the JVM defines them**. It is **not** a Spring AOP proxy factory. AspectJ LTW is one client of that SPI; JPA bootstrap is another (`LoadTimeWeaverAware`).

## What the weaver actually does

`org.springframework.instrument.classloading.LoadTimeWeaver` (Spring Framework 6.2) exposes `addTransformer`, `getInstrumentableClassLoader`, and `getThrowawayClassLoader`. The bean Spring registers is named **`loadTimeWeaver`**. Default implementation: **`DefaultContextLoadTimeWeaver`**, which picks an environment-specific delegate.

```d2
direction: down
cfg: "@EnableLoadTimeWeaving\nor context:load-time-weaver" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
bean: "loadTimeWeaver bean\n(DefaultContextLoadTimeWeaver)" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
hook: "Instrumentable ClassLoader\nor Instrumentation agent" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
xform: "ClassFileTransformer\n(e.g. AspectJ adapter)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
define: "defineClass → woven bytecode" {
  width: 280
  height: 45
  style.fill: "#fce4ec"
}

cfg -> bean
bean -> hook
hook -> xform
xform -> define
```

**Fig. 1.** The weaver does not advise calls. It registers transformers so **load** rewrites the class.

Autodetected delegates (when you keep the default weaver):

| Runtime | Delegate |
| --- | --- |
| Apache Tomcat | `TomcatLoadTimeWeaver` |
| GlassFish EAR | `GlassFishLoadTimeWeaver` |
| JBoss AS / WildFly | `JBossLoadTimeWeaver` |
| JVM with `spring-instrument.jar` agent | `InstrumentationLoadTimeWeaver` |
| Fallback (`addTransformer` on the ClassLoader) | `ReflectiveLoadTimeWeaver` |

Tomcat / JBoss / WildFly can instrument the webapp `ClassLoader` **without** `-javaagent`. A generic JVM (including a typical standalone Boot process) needs **`java -javaagent:…/spring-instrument.jar`**, which installs Spring’s **`InstrumentationSavingAgent`**. Vanilla AspectJ’s agent is **`aspectjweaver.jar`** — JVM-wide. Spring’s weaver is the per-`ClassLoader` hook; [[Why do you need a Java agent for load-time weaving]] is the agent half.

```java
@Configuration
@EnableLoadTimeWeaving
public class AppConfig {
}
```

**Listing 1.** Java form of `<context:load-time-weaver/>`. XML equivalent registers the same infrastructure. Needs an **`ApplicationContext`**: LTW setup uses `BeanFactoryPostProcessor`s, so a plain `BeanFactory` is not enough.

For AspectJ, Spring still needs **`spring-aop`** + **`aspectjweaver`** on the classpath, plus one or more **`META-INF/aop.xml`** files. The transformer that rewrites bytes is AspectJ’s `ClassPreProcessorAgentAdapter`; Spring only **adds** it. Details: [[How do you perform load-time weaving with AspectJ in a Spring application]], [[What is aop.xml for load-time weaving]], [[What is the EnableLoadTimeWeaving annotation]].

Any bean implementing **`LoadTimeWeaverAware`** receives the weaver after properties are set (JPA’s `LocalContainerEntityManagerFactoryBean` is the documented case). That path can use the weaver **without** AspectJ `aop.xml`.

> [!warning]Not a proxy factory
> **`@EnableAspectJAutoProxy`** still creates **JDK/CGLIB proxies** at runtime. The word “AspectJ” there is the **annotation style**, not this weaver. [[What is the difference between EnableLoadTimeWeaving and EnableAspectJAutoProxy]] and [[What is the difference between Spring AOP and AspectJ]]: Spring AOP never rewrites class files.

> [!warning]Annotation plus aop.xml is not an agent
> `@EnableLoadTimeWeaving` registers the bean. On a plain JVM, classes loaded **before** the weaver is hooked, or without an instrumentable loader / `spring-instrument` agent, stay **unwoven**. Interview lists of “compile-time / load-time / runtime weaving” mix **AspectJ bytecode modes** with **Spring AOP proxies** — only the first two are weaving.

> [!tip] Interview answer
> **A Spring `LoadTimeWeaver` adds `ClassFileTransformer`s to a class loader so bytecode can change at `defineClass`.** `@EnableLoadTimeWeaving` (or `<context:load-time-weaver/>`) publishes the `loadTimeWeaver` bean; AspectJ LTW then plugs in its adapter when `aop.xml` (or `aspectjWeaving = ENABLED`) says so. That is not Spring AOP. Proxies stay a separate runtime mechanism, and a generic JVM still needs `spring-instrument` or a container class loader that already supports transformers.
