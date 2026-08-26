<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #SRS

# How do you perform load-time weaving with AspectJ in a Spring application?

> [!abstract] Short answer
> Put **`aspectjweaver`** (and **`spring-aop`**) on the classpath, add **`META-INF/aop.xml`**, enable a **`LoadTimeWeaver`** with **`@EnableLoadTimeWeaving`** (or `<context:load-time-weaver/>`), and attach an **instrumentation hook**: **`-javaagent:…/spring-instrument.jar`** on a plain JVM, or a container weaver (Tomcat / WildFly) with **no** agent. This is **AspectJ bytecode LTW**, not Spring AOP proxies.

## Four pieces Spring actually documents

AspectJ aspects (code style or `@Aspect`) must be **compiled classes on the classpath**. Spring then:

1. Reads **`META-INF/aop.xml`** (standard AspectJ).
2. Registers **`ClassFileTransformer`s** via a **`LoadTimeWeaver`**.
3. Lets AspectJ’s `ClassPreProcessorAgentAdapter` rewrite classes **as they are defined**.

```xml
<aspectj>
	<weaver>
		<include within="com.xyz..*"/>
	</weaver>
	<aspects>
		<aspect name="com.xyz.ProfilingAspect"/>
	</aspects>
</aspectj>
```

**Listing 1.** Spring’s profiling example — declare the aspect and **limit** `include` to app packages (avoids dump files / noise). Default `aspectjWeaving` is **`AUTODETECT`**: weaving turns on if at least one `aop.xml` exists; use `aspectjWeaving = ENABLED` to force it, `DISABLED` to skip.

```java
@Configuration
@EnableLoadTimeWeaving
public class ApplicationConfiguration {
}
```

**Listing 2.** Registers `loadTimeWeaver` + `AspectJWeavingEnabler`. XML: `<context:load-time-weaver/>`. Needs an **`ApplicationContext`** (`BeanFactory` is not enough — LTW uses `BeanFactoryPostProcessor`s).

Jars: **`spring-aop`**, **`aspectjweaver`**, and **`spring-instrument`** if you use Spring’s agent. That agent is **`InstrumentationSavingAgent`** in **`spring-instrument.jar`**, not `aspectjweaver.jar` — vanilla AspectJ LTW uses the weaver jar as `-javaagent`; Spring’s generic-JVM example is:

```
java -javaagent:/path/to/spring-instrument.jar com.xyz.Main
```

Tomcat / JBoss / WildFly: **`TomcatLoadTimeWeaver`** / **`JBossLoadTimeWeaver`** — **no** launch-script agent. Why an agent exists at all: [[Why do you need a Java agent for load-time weaving]]. vs compile-time: [[What is the difference between compile-time and load-time weaving]].

```d2
direction: down
xml: "META-INF/aop.xml\n+ aspect classes" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
cfg: "@EnableLoadTimeWeaving\n(LoadTimeWeaver)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
hook: "spring-instrument agent\nor container ClassLoader" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
woven: "defineClass → woven bytecode" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}

xml -> cfg -> hook -> woven
```

**Fig. 1.** Full AspectJ LTW can advise **`new` objects that are not Spring beans** once the weaver is active (Spring’s `StubEntitlementCalculationService` example). Proxy AOP cannot — [[How do you enable AOP in a Spring application]].

> [!warning] `@EnableAspectJAutoProxy` is a different switch
> It builds **Spring AOP proxies**. It does **not** register the AspectJ class transformer. The two annotations are not interchangeable — [[What is the difference between EnableLoadTimeWeaving and EnableAspectJAutoProxy]].

> [!warning] Too late to weave already-defined classes
> AspectJ does not reweave classes **already defined** to the JVM. Start the **agent with the JVM** (or use a container weaver from the first load of the app `ClassLoader`). Turning on `@EnableLoadTimeWeaving` after those classes loaded does nothing to them.

> [!tip] Interview answer
> **LTW in Spring is `aop.xml` plus `@EnableLoadTimeWeaving` plus a class-load hook — usually `-javaagent:spring-instrument.jar`, or Tomcat’s instrumentable loader.** You still need `aspectjweaver`. That rewrites bytecode as classes load; `@EnableAspectJAutoProxy` only wraps beans in proxies.
