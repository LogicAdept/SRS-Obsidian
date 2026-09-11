<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What was new in Java 25

> [!abstract] Short answer
> **Java 25 (September 2025, LTS) finalized scoped values (JEP 506), flexible constructor bodies (513), module import declarations (511), and compact source files with instance main (512); made compact object headers a product feature (519) and Shenandoah generational (521); added Stable Values preview (502), PEM encodings preview (470), the KDF API (510), and a cluster of JFR upgrades (509/518/520) plus AOT method profiling (514/515). Structured concurrency is still preview (505).**

## The "small Java" LTS and the memory cut

The 512/511/513 trio modernizes how beginners and scripts look: a file with `void main()` runs (compact source files with implicitly declared classes), `import module java.base` replaces fifty single-type imports, and constructor validation can happen before `super()` ([[What are compact source files and instance main methods]], [[What are module import declarations]], [[What are flexible constructor bodies]]). Scoped values going final (506) completes the Loom context story — immutable, bounded-lifetime sharing designed for millions of virtual threads ([[What are scoped values]]). On the memory side, compact object headers (519) shrink the typical object header from 96 to 64 bits; generational Shenandoah (521) gives the third collector a young/old split. JFR CPU-time profiling (509), cooperative sampling (518), and method timing & tracing (520) push the observability line forward ([[How did JVM profiling and observability evolve after Java 8]]).

```java
public class V38_Kdf25 {
    public static void main(String[] args) {
        try {
            Class.forName("javax.crypto.KDF");            // JEP 510 KDF API: preview 24, final 25
            System.out.println("javax.crypto.KDF present");
        } catch (ClassNotFoundException e) {
            System.out.println("javax.crypto.KDF -> ClassNotFoundException on this JDK");
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V38_Kdf25 in empirics): `javax.crypto.KDF -> ClassNotFoundException on this JDK` (out/V38_Kdf25.txt) — the 25-era crypto API is version-detectable at runtime.

```d2
direction: right
fin: "scoped values FINAL (506)\nflexible ctor bodies FINAL (513)\nmodule imports (511)\ncompact source + instance main (512)" { style.fill: "#e8f5e9"; width: 330; height: 130 }
mem: "compact headers PRODUCT (519)\ngenerational Shenandoah (521)" { style.fill: "#e3f2fd"; width: 280; height: 90 }
obs: "JFR CPU-time (509), cooperative sampling (518)\nmethod timing (520), AOT profiling (514/515)" { style.fill: "#e3f2fd"; width: 360; height: 90 }
prev: "Stable Values preview (502)\nPEM preview (470)\nstructured concurrency 5th preview (505)" { style.fill: "#fff3e0"; width: 330; height: 90 }
fin -> mem -> obs -> prev: ""
```

**Fig. 1.** Java 25: the LTS that finalizes the beginner-syntax trio and scoped values, cuts memory, upgrades JFR, and keeps the big concurrency API previewing.

> [!warning] LTS does not mean everything final
> Even at 25, structured concurrency is on its fifth preview (505) and Stable Values debut as preview — the LTS mark is about support lifetime, not feature completeness ([[What is a preview feature in Java]]). And "scoped values final" is 25-precise: on 21 they were only preview (446).

> [!tip] Interview answer
> **Java 25 is the 2025 LTS: scoped values, flexible constructor bodies, module imports, and compact source files with instance main all finalized; compact object headers went product (96 to 64 bits) and Shenandoah became generational; JFR gained CPU-time profiling and method timing. Structured concurrency is still preview — the one Loom piece not yet final.**
