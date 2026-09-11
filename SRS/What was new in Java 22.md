<!--
reps: 0
priority: 0
-->
#Java/Versions/22 #SRS

# What was new in Java 22

> [!abstract] Short answer
> **Java 22 (March 2024) finalized the Foreign Function & Memory API (JEP 454) and unnamed variables & patterns (456), added the multi-file source launcher (458), G1 region pinning (423), and previewed the Class-File API (457), statements before super() (447), and stream gatherers (461). String templates got their second preview (459) — and were withdrawn one train later.**

## FFM final, JNI on notice

The FFM API going final (454) is the headline: `java.lang.foreign` with `Linker`, `Arena`, and `MemorySegment` gives native interop without `sun.misc.Unsafe` or JNI boilerplate, and the JVM enforces lifetime safety through arenas ([[What are unnamed variables and patterns]] is the syntax sibling that finalized here too). G1 region pinning (423) fixed a real latency wart: JNI `GetPrimitiveArrayCritical` pins could previously stall G1 collections; regions can now be pinned individually. The launcher upgrade (458) runs `java A.java` even when A references classes in sibling source files. On the unsafe path out: 23 deprecates the memory-access methods (471), 24 warns at their use (498).

```java
public class V35_Unnamed22 {
    static int count(String... parts) {
        int n = 0;
        for (var _ : parts) { n++; }         // element value not needed
        return n;
    }

    public static void main(String[] args) {
        try { Integer.parseInt("x"); } catch (NumberFormatException _) {
            System.out.println("caught, no name needed");   // JEP 443 preview (21) -> 456 final (22)
        }
        var _ = compute();                   // unnamed local: no warning, no name
        System.out.println("count=" + count("a", "b", "c"));
    }

    static int compute() { return 42; }
}
```

**Listing 1.** Verified on JDK 21 with `--enable-preview` (V35_Unnamed22 in empirics): `caught, no name needed`, `count=3` (out/V35_Unnamed22.txt) — previewed via 443 in 21, final in 22, no flag needed.

```d2
direction: right
final: "FFM FINAL (454)\nunnamed variables FINAL (456)\nmulti-file launcher (458)\nG1 region pinning (423)" { style.fill: "#e8f5e9"; width: 300; height: 120 }
prev: "Class-File API preview (457)\nstatements before super (447)\ngatherers preview (461)\nstring templates 2nd preview (459)" { style.fill: "#fff3e0"; width: 330; height: 120 }
final -> prev: ""
```

**Fig. 1.** Java 22: two finals on the interop/syntax side, a wide preview bench behind them.

> [!warning] String templates were still alive in 22
> 22 shipped their second preview (459) — and 23 withdrew them entirely (465). Any interview answer placing string templates in the timeline should stop at "previewed twice, withdrawn, never shipped" ([[What were string templates and why were they withdrawn]]).

> [!tip] Interview answer
> **Java 22 finalized the FFM API — the modern JNI replacement with arena-controlled memory lifetimes — and unnamed variables `_`. It added multi-file source launching and G1 region pinning, and previewed the Class-File API, statements before super(), and stream gatherers. String templates got a second preview here right before being withdrawn.**
