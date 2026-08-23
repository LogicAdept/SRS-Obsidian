<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #SRS

# Why do you need a Java agent for load-time weaving?

> [!abstract] Short answer
> **Load-time weaving (LTW) rewrites class bytecode as the JVM loads it**, which requires a hook into the class-loading pipeline — typically a **`java.lang.instrument` agent** (`-javaagent:…`) or an **instrumentable `ClassLoader`**. Vanilla AspectJ LTW uses **`aspectjweaver.jar`** as that agent. Spring's LTW usually uses **`spring-instrument.jar`** (or a container weaver such as **`TomcatLoadTimeWeaver`**) so weaving can be scoped per class loader — **`@EnableLoadTimeWeaving` alone does not attach any agent**.

## What LTW needs at load time

Spring's AspectJ LTW chapter defines load-time weaving as weaving AspectJ aspects into class files **as they are loaded into the JVM**. Something must register a **`ClassFileTransformer`** with the class loader before (or as) application classes are defined.

Two common hooks:

| Mechanism | Role |
|---|---|
| **`-javaagent:…`** | JVM agent gets `Instrumentation` and can transform all loaded classes |
| **Instrumentable ClassLoader** | Server/`ClassLoader` API (`addTransformer`) — Spring's environment-specific `LoadTimeWeaver`s |

```d2
direction: right
jvm: "JVM start" {
  width: 120
  height: 40
  style.fill: "#e3f2fd"
}
agent: "-javaagent\nor instrumentable CL" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
load: "ClassLoader.defineClass" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
weave: "Bytecode transformed\n(aspects applied)" {
  width: 200
  height: 60
  style.fill: "#fce4ec"
}

jvm -> agent -> load -> weave
```

**Fig. 1.** Without an instrumentation hook, classes load as compiled — no LTW occurs.

## AspectJ agent vs Spring agent vs no agent

**Vanilla AspectJ LTW** (no Spring): JVM-wide **`-javaagent:/path/to/aspectjweaver.jar`**. Coarse, but works without Spring.

**Spring-enabled LTW**: configure a **`LoadTimeWeaver`** (often via **`@EnableLoadTimeWeaving`**). Spring then adds AspectJ's transformer through that weaver.

- On a **plain JVM / unsupported ClassLoader**, Spring autodetection picks **`InstrumentationLoadTimeWeaver`**, which needs:
  ```
  -javaagent:/path/to/spring-instrument.jar
  ```
  (`InstrumentationSavingAgent` packaged in **`spring-instrument.jar`** — this is Spring's documented agent for that path, not a synonym for `aspectjweaver.jar`.)
- On **Tomcat / WildFly / …**, Spring can use **`TomcatLoadTimeWeaver`** / **`JBossLoadTimeWeaver`** and weave **without** changing the launch script to add `-javaagent`.

Trade-offs vs compile-time weaving: **no `ajc` in the build**, but **slower class loading**, a **JVM flag or server ClassLoader support**, and the agent/weaver must be present in **every environment** that should weave. See [[What is the difference between compile-time and load-time weaving]].

```java
@Configuration
@EnableLoadTimeWeaving
public class LtwConfig {
    // registers LoadTimeWeaver + AspectJ weaving enabler —
    // does NOT start a javaagent by itself
}
```

**Listing 1.** Annotation enables Spring's LTW beans; attach `-javaagent` (or use a container weaver) separately when required.

> [!warning] `@EnableLoadTimeWeaving` ≠ agent
> Enabling LTW in the application context **does not** inject `-javaagent`. On a stock HotSpot JVM without an instrumentable ClassLoader, weaving silently fails or aspects never apply until **`spring-instrument.jar`** (or AspectJ's weaver agent for pure AspectJ LTW) is on the command line. Keep **`META-INF/aop.xml`** (or equivalent) as well — see [[What is the EnableLoadTimeWeaving annotation]] and [[How do you perform load-time weaving with AspectJ in a Spring application]].

> [!tip] Interview answer
> LTW transforms classes while they load, so the JVM needs an instrumentation hook — usually a Java agent. Pure AspectJ uses aspectjweaver.jar; Spring LTW typically uses spring-instrument.jar with InstrumentationLoadTimeWeaver, or a container ClassLoader weaver so you can skip -javaagent. @EnableLoadTimeWeaving configures Spring; it does not attach the agent.
