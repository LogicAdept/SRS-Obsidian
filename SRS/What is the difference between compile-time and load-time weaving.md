<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is the difference between compile-time and load-time weaving?

> [!abstract] Short answer
> Both are **AspectJ bytecode weaving** and produce the **same** woven class files. **Compile-time** (`ajc`) weaves while compiling source. **Load-time (LTW)** defers that **binary** weave until a class loader **defines** the class (agent or weaving loader + `aop.xml`). **Spring AOP proxies are neither.** Post-compile (weave existing JARs) is a third AspectJ time, not LTW.

## Same weaver, different clock

AspectJ: class files in → class files out. Runtime behavior does **not** depend on *when* you wove.

**Compile-time:** `ajc` compiles and weaves in one step. Aspects may be source or binary. You **must** weave at compile-time if other types **reference members the aspect introduces** (those types cannot compile against unwoven sources).

**Load-time:** the same binary weave, **later** — when the class is defined to the JVM. Needs a **weaving class loader** or **`-javaagent:…/aspectjweaver.jar`**, and `META-INF/aop.xml`. Spring can drive this per class loader (`LoadTimeWeaver`, `@EnableLoadTimeWeaving`) instead of a JVM-wide AspectJ agent — [[How do you perform load-time weaving with AspectJ in a Spring application]], [[Why do you need a Java agent for load-time weaving]].

**Post-compile (binary):** weave existing `.class`/JAR without waiting for class load. Dumps often fold this into “compile-time.” It is still **before** those classes run, not LTW.

```d2
direction: down
ctw: "Compile-time\najc: source → woven .class" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ltw: "Load-time\ndefineClass → woven bytes in VM" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
same: "Same woven semantics\n(AspectJ weaver output)" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}

ctw -> same
ltw -> same
```

**Fig. 1.** Choose *when* the weaver runs, not a different AOP model. Spring’s default path is a **runtime proxy**, which never rewrites the target — [[What is weaving in AOP]], [[How does Spring AOP work internally]].

| | Compile-time | Load-time |
| --- | --- | --- |
| **Input** | Source (+ optional binary aspects) | Already-compiled class files |
| **When** | Build | Class load / `defineClass` |
| **Tooling** | `ajc` / AspectJ Maven/Ant | Agent, weaving loader, or Spring `LoadTimeWeaver` |
| **3rd-party JARs** | Use **post-compile** binary weave | LTW if the loader can see them |

> [!warning] Spring `@Aspect` is still proxies
> `@EnableAspectJAutoProxy` does **not** turn on CTW or LTW. Use AspectJ weaving when you need join points proxies cannot see (self-invocation, constructors, non-beans).

> [!warning] Introductions can force compile-time
> If code must **compile against** ITD members, LTW is too late — those types never compiled. LTW also cannot weave classes **already defined** in the JVM (AspectJ has no “run-time weaving” of loaded classes).

> [!tip] Interview answer
> **Compile-time weaving runs `ajc` at the build; load-time weaving runs the same bytecode weaver when the class is loaded.** Woven behavior matches. Spring AOP is a third option: runtime proxies, no class-file rewrite.
