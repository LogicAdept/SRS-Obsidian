<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is weaving in AOP?

> [!abstract] Short answer
> **Weaving** is **linking aspects with types or objects** so you get an **advised** object. AspectJ weaves **bytecode** at **compile time**, **post-compile** (binary/JAR), or **load time**. **Spring AOP** weaves at **runtime** by wrapping beans in **proxies** — it does **not** rewrite the target class.

## When the aspect is attached

Spring *AOP Concepts*: weaving can happen at compile time (e.g. the AspectJ compiler), load time, or runtime. **Spring AOP, like other pure Java AOP frameworks, performs weaving at runtime.**

AspectJ’s weaver takes **class files in** and **class files out**. The woven bytes (and thus runtime behavior) are the **same** whichever of these three times you pick:

| When | What happens |
| --- | --- |
| **Compile-time** | `ajc` compiles source and weaves in one step. Required if other code must see members the aspect **introduces**. |
| **Post-compile (binary)** | Weave existing `.class` / JAR files. Aspects may themselves be already woven. |
| **Load-time (LTW)** | Same binary weaving, **deferred** until a class loader **defines** the class. Needs a weaving class loader or **`-javaagent:…/aspectjweaver.jar`**, plus `META-INF/aop.xml`. |

AspectJ 5’s “run-time weaving” means rewriting classes **already defined** to the JVM. **It does not support that.** Spring’s “runtime weaving” is a **different** mechanism: a JDK or CGLIB **proxy** around a Spring bean — [[How does Spring AOP work internally]].

```d2
direction: down
aj: "AspectJ weaver\n(compile / post-compile / load)" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
bc: "Target class bytecode\ncontains the advice" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
spring: "Spring AOP runtime\nproxy around unchanged class" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}

aj -> bc
spring -> bc: "does not rewrite"
```

**Fig. 1.** Bytecode weaving vs proxy wrapping. AspectJ CTW/LTW apply advice **inside** the class, so `this.foo()` is advised; Spring proxies are not — [[What is the difference between Spring AOP and AspectJ]].

Spring can still **drive AspectJ LTW** (`LoadTimeWeaver`, `@EnableLoadTimeWeaving`) as a **separate** mode from `@EnableAspectJAutoProxy`. How to set that up: [[How do you perform load-time weaving with AspectJ in a Spring application]].

> [!warning] “Spring supports three weaving times” is a dump mix-up
> **Spring AOP** = runtime **proxies** only. Compile-time and load-time are **AspectJ**. Using `@Aspect` pointcut syntax does not switch you to bytecode weaving.

> [!warning] Load-time is not “runtime weaving”
> LTW still **rewrites class files as they load**. Classes already defined in the JVM are not rewoven (AspectJ). Missing the agent / `aop.xml` means **no** weave, not a silent fallback to Spring proxies.

> [!tip] Interview answer
> **Weaving is attaching aspects to types to produce an advised object.** AspectJ does it by rewriting bytecode at compile, post-compile, or class-load time. Spring AOP does it at runtime with proxies and leaves the target class unchanged.
