<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the difference between EnableLoadTimeWeaving and EnableAspectJAutoProxy?

> [!abstract] Short answer
> **`@EnableAspectJAutoProxy`** turns on **Spring AOP proxies** for `@Aspect` beans. The “AspectJ” in the name is the **annotation/pointcut style**, not the weaver. **`@EnableLoadTimeWeaving`** registers a **`LoadTimeWeaver`** so **AspectJ can rewrite class bytecode at load time**. They are **not** substitutes. You can enable both; each path stays distinct.

## Two switches, two runtimes

Spring’s XML note for `<aop:aspectj-autoproxy/>` applies to the annotation too: **Spring AOP proxies**, **AspectJ runtime not involved**. Javadoc: `@EnableAspectJAutoProxy` processes `@Aspect` components and **proxies** matching beans (`FooService` in the sample). Needs **`aspectjweaver`** for pointcut parsing. Local to **that** `ApplicationContext`.

`@EnableLoadTimeWeaving` is the Java form of `<context:load-time-weaver/>`: a bean named **`loadTimeWeaver`**, plus optional AspectJ LTW. `aspectjWeaving` default **`AUTODETECT`** — on if **`META-INF/aop.xml`** exists. **`ENABLED`** forces the AspectJ transformer; **`DISABLED`** skips it. XML `aspectj-weaving="on"` also enables `@Configurable` support; **`@EnableLoadTimeWeaving(aspectjWeaving=ENABLED)` does not** — you add `@EnableSpringConfigured` yourself.

```java
@Configuration
@EnableAspectJAutoProxy
class ProxyAopConfig { }

@Configuration
@EnableLoadTimeWeaving // AUTODETECT if aop.xml present
class LtwConfig { }
```

**Listing 1.** Same `@Aspect` types can feed **either** path. Auto-proxy still only advises **Spring beans** through a proxy. LTW can advise **`new` instances** once the weaver is on the class loader — [[How do you perform load-time weaving with AspectJ in a Spring application]], [[How do you enable AOP in a Spring application]].

| | `@EnableAspectJAutoProxy` | `@EnableLoadTimeWeaving` |
| --- | --- | --- |
| **Mechanism** | JDK / CGLIB **proxy** | **`ClassFileTransformer`** (AspectJ LTW) |
| **XML twin** | `<aop:aspectj-autoproxy/>` | `<context:load-time-weaver/>` |
| **Extra hook** | Aspect beans in the context | Agent or instrumentable **ClassLoader**, `aop.xml` |
| **Self-invocation** | Skips advice | Advised (bytecode) |

Mixing: Spring AOP can **include** only some `@Aspect` bean names so LTW aspects are not also auto-proxied. Annotation details: [[What is the EnableAspectJAutoProxy annotation]].

```d2
direction: right
proxy: "@EnableAspectJAutoProxy\nproxy around bean" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ltw: "@EnableLoadTimeWeaving\nweave at defineClass" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

proxy -> ltw: "orthogonal"
```

**Fig. 1.** Enabling both does not merge them. Missing `aop.xml` / agent leaves **LTW off** (`AUTODETECT`) while **auto-proxy still wraps beans**.

> [!warning] The word AspectJ on auto-proxy is a naming trap
> `@EnableAspectJAutoProxy` never starts the AspectJ weaver. Boot’s AOP starter typically turns **this** on, not LTW.

> [!warning] `ENABLED` is not an agent
> `aspectjWeaving = ENABLED` only registers the transformer **on Spring’s `LoadTimeWeaver`**. On a plain JVM you still need **`-javaagent:spring-instrument.jar`** (or a container weaver). Classes already defined are not rewoven.

> [!tip] Interview answer
> **`@EnableAspectJAutoProxy` is Spring AOP — proxies that understand `@Aspect`.** **`@EnableLoadTimeWeaving` is the class-load weaver hook.** Same annotation style, different runtime. Name does not mean bytecode weaving is on.
