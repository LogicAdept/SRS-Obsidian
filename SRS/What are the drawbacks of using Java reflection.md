<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS

# What are the drawbacks of using Java reflection?

> [!abstract] Short answer
> **It is slower than a compiled call, it can be forbidden or abused around access control, and it breaks the abstractions the compiler normally enforces.** The Oracle Reflection trail’s three concerns are **performance overhead**, **security restrictions**, and **exposure of internals**. If the same work can be done without reflection, do that.

## Three documented costs

Reflection examines and calls members of **loaded** classes through `Class` / `java.lang.reflect`. That is powerful for tools and serializers ([[What are some use cases of Java reflection]], [[What is reflection in Java]]). It is also a path the language normally closes.

```d2
direction: down
use: "Reflective call / field access" {
  width: 260
  height: 50
}
perf: "No static call shape\nVM optimizations skipped" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
sec: "Needs suppressAccessChecks\nor is denied (modules / SM)" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
enc: "private becomes reachable\nabstractions leak" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
use -> perf
use -> sec
use -> enc
```

**Fig. 1.** Trail drawbacks: speed, permission/encapsulation, internals. Same APIs that enable plugins also skip compile-time checks.

**Performance.** Types are resolved at runtime, so some JVM optimizations that apply to ordinary invokes cannot run. Reflective operations are **slower** than the equivalent compiled call or field access. The trail says to avoid them in **frequently executed**, performance-sensitive code.

**Security and access.** `setAccessible(true)` suppresses Java language access checks when `ReflectPermission("suppressAccessChecks")` is granted ([[What does setAccessible do in the Reflection API]]). Under a security manager that permission may be **absent**. On the module path, a package that is not **open** yields `InaccessibleObjectException` instead of a silent bypass. Reflection is therefore both a way to reach `private` members **and** a surface that restricted environments clamp down on.

**Exposure of internals.** Private fields and methods can be used in ways that would not compile. That can cause unexpected side effects, break portability, and **change behavior when the platform upgrades** — reflective code is coupled to layout the compiler would have hidden. `Field.set` on a (non-static) `final` is documented as meaningful mainly for deserialization; other use may keep showing the old value ([[Can you change the value of a final field using reflection]], [[How do you invoke a private constructor using reflection]]).

```java
class Fragile {
    static Object call(Object target) throws Exception {
        Method m = target.getClass().getMethod("process", String.class);
        return m.invoke(target, "x");
    }
}
```

**Listing 1.** `"process"` is a string. Rename the method and this still **compiles**; it fails at runtime with `NoSuchMethodException` ([[How can you invoke a method using reflection]]). Direct `target.process("x")` would have been a compile error.

> [!warning] Prefer a normal call when the type is in the source
> The trail’s rule is not “never reflect.” It is: if the operation is possible without reflection, **prefer that**. Everyday application code that already depends on a type should call it, not look it up by name.

> [!warning] Encapsulation is not a suggestion to `setAccessible`
> Reaching `private` state can expose secrets and violate invariants (singletons, records, module boundaries). Frameworks that do this still pay the costs; they do not make those costs disappear.

> [!tip] Interview answer
> **Slower than direct calls, extra permissions or module opens, and you lose compile-time checking — names are strings, so breakage is `NoSuchMethodException` at runtime.** You can also pierce `private` and freeze assumptions that break on a JDK upgrade. **Use it for tools, serializers, and true runtime types; not as the default way to call a class you already import.**
