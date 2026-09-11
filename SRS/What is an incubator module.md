<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is an incubator module

> [!abstract] Short answer
> **An incubator module (JEP 11) is a non-standard JDK module holding an immature API: `jdk.incubator.*` names like `jdk.incubator.vector`, resolved only with `--add-modules`, and explicitly allowed to change or vanish between releases.** The Vector API has incubated since 16 (eleventh incubator by 26); the Foreign Function & Memory API incubated 14–21, then finalized as `java.lang.foreign` in 22. Incubator is for API experimentation; preview is for language/API shape-testing behind a flag ([[What is a preview feature in Java]]).

## Mechanics

An incubator module is a real JPMS module that ships inside the JDK image but is **not resolved by default** and is not part of the Java SE specification. You opt in per process: `javac --add-modules jdk.incubator.vector` and `java --add-modules jdk.incubator.vector` (or `@Incubator` warnings on the classpath path). Because the API carries no compatibility guarantee, code compiled against one JDK's incubator module may fail to compile on the next — each round is a new module version. When the API matures it graduates: it is standardized, the incubator copy is removed, and the package is usually renamed (Panama's `jdk.incubator.foreign` became `java.lang.foreign` at 22).

Graduation history worth citing: Vector API (JEP 338, first incubator in 16; still incubating in 26 — a rare long resident) versus Foreign Function & Memory (incubators 14–21, JEP 454 final in 22). Long residence is the signal that the design itself is still contested ([[What is the Java Platform Module System]]).

```d2
direction: down
inc: "jdk.incubator.*\nno compat guarantee\n--add-modules to resolve" {
  width: 320
  height: 70
  style.fill: "#fff8e1"
}
a: "change between releases" {
  width: 250
  height: 50
  style.fill: "#fff3e0"
}
b: "disappear entirely" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
grad: "graduate -> standard API\nFFM: java.lang.foreign (22)" {
  width: 300
  height: 65
  style.fill: "#e8f5e9"
}
inc -> a
inc -> b
inc -> grad
```

**Fig. 1.** Three legal outcomes for an incubating API: churn, removal, or graduation into `java.*`. Only graduation is a happy ending for adopters.

```java
import jdk.incubator.vector.IntVector;
import jdk.incubator.vector.VectorSpecies;

public class V06_Incubator {
    private static final VectorSpecies<Integer> SPECIES = IntVector.SPECIES_PREFERRED;

    public static void main(String[] args) {
        int[] a = {1, 2, 3, 4, 5, 6, 7, 8};
        int[] b = {10, 20, 30, 40, 50, 60, 70, 80};
        int[] c = new int[a.length];
        for (int i = 0; i < a.length; i += SPECIES.length()) {
            var lane = SPECIES.loopBound(a.length - i) >= SPECIES.length()
                    ? IntVector.fromArray(SPECIES, a, i).mul(IntVector.fromArray(SPECIES, b, i))
                    : null;
            if (lane != null) {
                lane.intoArray(c, i);
            } else {
                for (int j = i; j < a.length; j++) c[j] = a[j] * b[j];
            }
        }
        System.out.println(java.util.Arrays.toString(c));
        Module m = IntVector.class.getModule();
        System.out.println("module name: " + m.getName());
        System.out.println("isExported to everyone: " + m.isExported("jdk.incubator.vector"));
    }
}
```

**Listing 1.** Verified on JDK 21 with `--add-modules jdk.incubator.vector` (V06_Incubator in empirics): `[10, 40, 90, 160, 250, 360, 490, 640]`, `module name: jdk.incubator.vector`, `isExported to everyone: true` — plus the startup `WARNING: Using incubator modules: jdk.incubator.vector` reminding you nothing here is standard (out/V06_Incubator.txt).

> [!warning] Incubator code is throwaway by design
> Shipping incubator API use to production is the trap: the warning is not decoration, and a JDK upgrade can break the build with no deprecation notice at all. The second trap is mixing up the two experimentation channels — incubator modules are **API** experiments needing `--add-modules`; preview features are language/API drafts needing `--enable-preview` and version-locked bytecode. Vector API incubating since 16 is the standing counterexample to "incubator means next release it's final."

> [!tip] Interview answer
> **Incubator modules are `jdk.incubator.*` JDK modules for immature APIs — opted in with `--add-modules`, no compatibility promise, expected to change or vanish.** Vector API has incubated since 16; the FFM API incubated through 21 and graduated as `java.lang.foreign` in 22. Fine for benchmarks, never for production.
