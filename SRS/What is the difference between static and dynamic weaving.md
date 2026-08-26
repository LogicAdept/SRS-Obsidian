<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is the difference between static and dynamic weaving?

> [!abstract] Short answer
> Interview “**static weaving**” means **AspectJ bytecode weaving** (`ajc` compile-time or post-compile): the aspect is **in the class file** before the JVM runs your code. Interview “**dynamic weaving**” usually means **Spring AOP runtime proxies** — a JDK/CGLIB wrapper, **no** rewrite of the target class. Official names are **compile-time / post-compile / load-time** (AspectJ) vs **runtime proxy weaving** (Spring AOP). **Load-time weaving is still bytecode weaving**, not Spring proxies.

## Map dump words to the real mechanisms

AspectJ’s weaver always takes **class files in** and **class files out**. It can run at **compile-time**, **post-compile** (binary/JAR), or **load-time**. The woven bytes are the **same** whichever of those three you pick. AspectJ 5 does **not** weave classes **already defined** to the JVM (“run-time weaving” in their glossary).

Spring *AOP Concepts*: **Spring AOP weaves at runtime** by creating an advised **proxy**. That is **not** the AspectJ weaver.

| Interview phrase | What actually happens |
| --- | --- |
| **Static weaving** | AspectJ **`ajc`** / binary weaver **rewrites** target bytecode before (or as) you ship it. Needs the AspectJ compiler/weaver, not `javac` alone. |
| **Dynamic weaving** (dumps) | **Spring AOP**: `BeanPostProcessor` wraps a bean in a **JDK or CGLIB proxy**. Target class bytes stay as `javac` left them. |
| **Load-time weaving** | Same **binary** weave as static, **deferred** until the class loader **defines** the class (`-javaagent` / weaving loader, `aop.xml`). |

```d2
direction: right
stat: "Bytecode weave\n(compile / post-compile / LTW)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
dyn: "Spring AOP proxy\n(runtime, class unchanged)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}

stat -> dyn: "different mechanism"
```

**Fig. 1.** Do not treat LTW as “the dynamic one.” LTW still **instruments bytecode**; Spring AOP **does not**. Definitions: [[What is weaving in AOP]]. CTW vs LTW: [[What is the difference between compile-time and load-time weaving]]. Proxies: [[How does Spring AOP work internally]].

AspectJ CTW/LTW put advice **inside** the class (`this.foo()` is advised). Spring proxies do not — [[What is the difference between Spring AOP and AspectJ]].

> [!warning] “Static vs dynamic” is not AspectJ’s weave-time vocabulary
> AspectJ documents **compile-time, post-compile, load-time**. “Static/dynamic” in AspectJ more often means **pointcut match**: a **dynamic** match cannot be decided from the bytecode shadow alone, so the weaver inserts a **runtime test**. That is unrelated to Spring proxies.

> [!warning] Do not promise “static is faster”
> AspectJ states woven class files are equivalent across its three weave times. Spring proxy dispatch is a **different** cost model (interceptor chain per call). There is no official “static weaving always wins” number.

> [!tip] Interview answer
> **Say bytecode weaving versus Spring proxies, not just static versus dynamic.** AspectJ bakes advice into class files at compile, post-compile, or class-load time. Spring AOP wraps beans at runtime and never rewrites the target. Load-time weaving is still AspectJ bytecode, not a proxy.
