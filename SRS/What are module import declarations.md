<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What are module import declarations

> [!abstract] Short answer
> **JEP 511 (final in Java 25; previewed in 23/24 as 476/494) adds `import module M`: all of the module's exported packages — plus the exports of everything it pulls in via `requires transitive` — come into scope for on-demand single-type use, like wildcard imports per package. A single-type import always wins over ambiguous module imports.**

## What it changes in source

Before: `import java.util.List; import java.util.stream.Collectors; ...` or the per-package on-demand `import java.util.*;`. Now: one `import module java.base;` covers all ~54 exported packages of `java.base`, including `java.time`, `java.util`, `java.io`, `java.nio`. It is name resolution sugar only — nothing changes in bytecode, classpath, or module deps; the code still compiles to the same explicit references. Ambiguity: if `import module java.base` and `import module java.desktop` both offer `List` (awt also has one), an unqualified `List` is a compile error until a single-type import `import java.util.List;` disambiguates — that rule keeps resolution deterministic ([[What is the Java Platform Module System]] for the underlying model).

```java
public class V48_ModuleImports {
    public static void main(String[] args) {
        Module base = ModuleLayer.boot().findModule("java.base").orElseThrow();
        long exported = base.getDescriptor().exports().stream()
                .filter(e -> !e.isQualified()).count();
        System.out.println("java.base unqualified exported packages = " + exported);
        // import module java.base (JEP 511, final in 25; previews 476/494) puts all of
        // these packages on the import path at once; a single-type import wins on clashes.
    }
}
```

**Listing 1.** Verified on JDK 21 (V48_ModuleImports in empirics): `java.base unqualified exported packages = 54` (out/V48_ModuleImports.txt) — the scope one `import module java.base` statement pulls in on a 25-era source file.

```d2
direction: right
stmt: "import module java.base;" { style.fill: "#e8f5e9"; width: 250; height: 60 }
exp: "all exported packages of java.base\n(+ transitive requires)" { style.fill: "#e3f2fd"; width: 320; height: 80 }
use: "List, Map, Instant, Path ...\nresolve on demand" { style.fill: "#fff3e0"; width: 270; height: 80 }
amb: "name clash? one single-type\nimport decides" { style.fill: "#ffebee"; width: 280; height: 70 }
stmt -> exp -> use -> amb: ""
```

**Fig. 1.** Resolution pipeline of a module import: one statement, whole-module scope, deterministic tie-breaking.

> [!warning] Module import is not a dependency grant
> It only widens name resolution: you cannot use `import module java.sql` to bypass missing `requires` clauses at compile time in a module-info world, and it does not load anything new at runtime. The common misread is "it imports the module like a JPMS requires" — `requires` stays the dependency statement ([[What was new in Java 25]] pairs it with JEP 512's implicit import).

> [!tip] Interview answer
> **Module import declarations — JEP 511, final in 25 — let one line, import module java.base, put every exported package into name-resolution scope, including transitive exports. It is pure sugar over the same bytecode, and clashes resolve by preferring explicit single-type imports. It previewed in 23 and 24 and lands alongside compact source files to cut beginner ceremony.**
