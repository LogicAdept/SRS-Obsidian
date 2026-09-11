<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# How does Java version numbering work

> [!abstract] Short answer
> **Java's numbers changed schemes twice.** Classic releases were `1.0`–`1.4`, then marketing renamed `1.5`→"Java 5" and `1.6`→"Java 6" while `java.version` still reported `1.5.0` / `1.6.0`; Java 7 and 8 kept `1.7` / `1.8` in properties. Since **JDK 9** (JEP 223) the version is a single rising number with a semantic format `$FEATURE.$INTERIM.$UPDATE.$PATCH` (JEP 322 added the cadence semantics), and `Runtime.Version` exposes the components.

## Reading a modern version string

JEP 223 (JDK 9) switched the numbering so the **feature** number is the release itself: 9, 10, 11 … 25. The full string is `FEATURE.INTERIM.UPDATE.PATCH` plus build and optional pre-release info — `21.0.12.1+1-LTS` is feature 21, interim 0, update 12, patch 1, build 1, with vendor decoration. `Runtime.Version` (since 9) parses it: `feature()`, `interim()`, `update()`, `patch()`, `pre()`, `build()`. JEP 322 (JDK 10) tied the scheme to the time-based train so the feature number rises every six months ([[What is the Java release cadence since Java 9]]).

The legacy trap lives in system properties, not in `Runtime.Version`: on Java 8, `java.version` is `1.8.0_412`, `java.specification.version` is `1.8`, and `java.vm.version` carries the HotSpot build. Scripts and parsers written for the `1.x` world break on `9+` when they expect a leading `1.` — and the reverse breaks too ([[What is an LTS release of Java]]).

```d2
direction: down
old: "pre-9 strings\njava.version = 1.8.0_412\nspec.version = 1.8" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
jep223: "JEP 223 (JDK 9)\nfeature number = release\n9, 10, 11 …" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
jep322: "JEP 322 (JDK 10)\nFEATURE.INTERIM.UPDATE.PATCH\nevery six months" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
rt: "Runtime.Version\nfeature() interim() update() patch()\npre() build()" {
  width: 340
  height: 70
  style.fill: "#f3e5f5"
}
old -> jep223 -> jep322 -> rt
```

**Fig. 1.** Two scheme changes: marketing numbers over `1.x`, then the single-number cadence scheme with `Runtime.Version` as the parser.

```java
public class V03_Numbering {
    public static void main(String[] args) {
        Runtime.Version v = Runtime.version();
        System.out.println("toString: " + v);
        System.out.println("feature: " + v.feature());
        System.out.println("interim: " + v.interim());
        System.out.println("update: " + v.update());
        System.out.println("patch: " + v.patch());
        System.out.println("pre: " + v.pre());
        System.out.println("build: " + v.build());
        System.out.println("prop java.version: " + System.getProperty("java.version"));
        System.out.println("prop java.specification.version: " + System.getProperty("java.specification.version"));
        System.out.println("prop java.vm.version: " + System.getProperty("java.vm.version"));
    }
}
```

**Listing 1.** Verified on JDK 21 (V03_Numbering in empirics): `toString: 21.0.12.1+1-LTS`, `feature: 21`, `interim: 0`, `update: 12`, `patch: 1`, `pre: Optional.empty`, `build: Optional[1]`, `prop java.specification.version: 21` — on Java 8 the same properties would read `1.8.0_xxx` and `1.8` (out/V03_Numbering.txt).

> [!warning] Parsing `1.x`-era properties is the classic break
> Checking `java.specification.version.startsWith("1.")` breaks on 9+ (it is `21`, not `1.21`), and checking `equals("21")` breaks on 8 (`1.8`). The robust pattern since 9 is `Runtime.version().feature() >= N`; on Java 8 you must special-case `1.8`. Another lie to avoid: "Java 5 was the fifth release" — internally it was 1.5, and Oracle's marketing number ran ahead of the property value until the schemes merged at 9.

> [!tip] Interview answer
> **Pre-9 releases carried `1.x` versions — Java 8 still reports `1.8.0` — while JEP 223/322 made the number a single rising feature counter with `$FEATURE.$INTERIM.$UPDATE.$PATCH` since 9.** `Runtime.Version` parses it (`feature()` gives 21 for `21.0.12.1`). Migration code must handle both the `1.8` and `9+` forms.
