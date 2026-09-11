<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What is the Java Platform Module System

> [!abstract] Short answer
> **JPMS (JEP 261, Java 9) is the module system for the platform itself: a `module-info.java` declares what a module `requires`, which packages it `exports` for compile-time use, `opens` for deep reflection, and `provides`/`uses` services.** It delivers reliable configuration (no more jar-hell classpath scanning) and strong encapsulation — non-exported packages are inaccessible even reflectively unless opened, which culminated in the 16/17 strong-encapsulation default for JDK internals ([[What is strong encapsulation of JDK internals]]).

## How a module is built

`module-info.java` sits at the module root. `requires` (optionally `static` for optional, or `transitive` to propagate to readers) names dependencies; `exports p` makes package `p` public-API visible; `exports p to m` qualifies it; `opens p` (or `opens p to m`) permits runtime reflection — `setAccessible` — without compile visibility; `provides S with I` / `uses S` wire `ServiceLoader`. The JDK itself is modularized from `java.base` up, and `jlink` assembles trimmed custom runtimes from module graphs. Classes left on the classpath live in the **unnamed module**, which reads everything and exports everything — that is why old jar applications still run while the JDK's own internals got sealed.

`setAccessible(true)` on a non-opened package throws `InaccessibleObjectException`; classpath frameworks hit exactly that against JDK internals on 16+ ([[What does setAccessible do in the Reflection API]]). Named-module visibility is checked at both compile time and run time — the compiler sees only `exports`, reflection only `opens`.

```d2
direction: down
app: "module com.app {\n  requires com.greet;\n}" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
greet: "module com.greet {\n  exports com.greet.api;\n  // com.greet.internal NOT exported\n}" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
unnamed: "classpath jars -> unnamed module\nreads everything, exports everything" {
  width: 380
  height: 70
  style.fill: "#fff8e1"
}
app -> greet: "compile: exports\nreflect: opens"
greet -> unnamed: "separate worlds"
```

**Fig. 1.** Visibility is per-package and per-direction: `exports` for callers, `opens` for reflectors; the unnamed module keeps legacy jars running.

```java
// Listing 1 — real two-module build (sources shown verbatim):
// src/com.greet/module-info.java
module com.greet {
    exports com.greet.api;
}
// src/com.greet/com/greet/api/Greeter.java
package com.greet.api;
public class Greeter {
    public String greet(String name) { return "hello, " + name; }
}
// src/com.app/module-info.java
module com.app {
    requires com.greet;
}
// src/com.app/com/app/Main.java
package com.app;
import com.greet.api.Greeter;
public class Main {
    public static void main(String[] args) {
        System.out.println(new Greeter().greet("jpms"));
        Module g = Greeter.class.getModule();
        System.out.println("module: " + g.getName() + " exports com.greet.api to caller: "
                + g.isExported("com.greet.api", Main.class.getModule()));
    }
}
```

**Listing 1.** Verified on JDK 21 (V11_Jpms in empirics, compiled with `--module-source-path`, run with `java -p modsout -m com.app/com.app.Main`): `hello, jpms`, `module: com.greet exports com.greet.api to caller: true` — a named module graph with an explicit boundary (out/V11_Jpms.txt).

> [!warning] Modules do not make jars disappear — and `opens` is not `exports`
> The common overreach: "JPMS means the classpath is dead." Classpath jars land in the unnamed module and run exactly as before — modules are opt-in for application code until you ship `module-info`. The second trap: `exports` and `opens` are different grants — an exported package is still closed to `setAccessible` reflection unless also opened, which is why frameworks crash with `InaccessibleObjectException` on 17 despite "it's a public API." And OSGi-style dynamic versioning is not part of JPMS; module resolution has no versions ([[What is strong encapsulation of JDK internals]]).

> [!tip] Interview answer
> **JPMS is the Java 9 module system: module-info with requires/exports/opens/provides, giving reliable configuration and strong encapsulation.** The JDK itself is modularized (java.base), jlink builds trimmed runtimes, classpath code runs as the unnamed module. Follow-up: exported is not opened — reflective frameworks need `opens` or `--add-opens`, which is exactly what hardened in 16/17.
