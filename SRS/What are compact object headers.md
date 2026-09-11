<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What are compact object headers

> [!abstract] Short answer
> **Compact object headers (Project Lilliput; experimental JEP 450 in Java 24, product JEP 519 in Java 25) shrink the HotSpot object header from 96 bits to 64 by folding the compressed class pointer into the mark word. The typical small object loses eight bytes of footprint, improving density, cache behavior, and GC throughput; the change is guarded by `-XX:+UseCompactObjectHeaders`.**

## What the header held and what moved

A 64-bit HotSpot object historically carried two machine words before any field: a mark word (identity hash, GC age bits, lock state) plus a klass pointer (or compressed 32-bit reference to class metadata) — 96 bits with compressed oops. Lilliput's trick: store the class pointer inside the mark word's unused bits, keeping a single 64-bit header, with lock state designed so biased locking's absence (disabled since 15) leaves room. Every object in a large heap loses eight bytes: an `Integer` drops from 16 to 12 bytes of footprint, dense data structures shrink, and allocation rate per cache line improves. The flag probe is version archaeology in one line: on 21 the option does not exist ([[How do you calculate the memory footprint of a Java object]], [[What was new in Java 24]]).

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;

public class V50_CompactHeaders25 {
    public static void main(String[] args) throws Exception {
        var jdk = System.getProperty("java.home") + "/bin/java";
        var p = new ProcessBuilder(List.of(jdk, "-XX:+UseCompactObjectHeaders", "-version"))
                .redirectErrorStream(true).start();
        String out;
        try (var r = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
            out = r.lines().collect(java.util.stream.Collectors.joining(" | "));
        }
        System.out.println("exit=" + p.waitFor());
        System.out.println("output=" + out);
    }
}
```

**Listing 1.** Verified on JDK 21 (V50_CompactHeaders25 in empirics): `exit=1`, `output=Unrecognized VM option 'UseCompactObjectHeaders' | Error: Could not create the Java Virtual Machine. | Error: A fatal exception has occurred. Program will exit.` (out/V50_CompactHeaders25.txt) — the feature postdates 21; experimental in 24, product in 25.

```d2
direction: right
old: "header 96 bits\nmark word (64)\n+ klass ptr (32, compressed)" { style.fill: "#ffebee"; width: 260; height: 100 }
new: "header 64 bits\nmark word with folded\nclass pointer + lock state" { style.fill: "#e8f5e9"; width: 280; height: 100 }
res: "8 bytes saved per object\nbetter density + cache use" { style.fill: "#e3f2fd"; width: 280; height: 100 }
old -> new -> res: ""
```

**Fig. 1.** The header compaction: two machine words become one, and the saving multiplies across the heap.

> [!warning] Footprint numbers are header-only, not object-size guarantees
> Alignment padding means some objects save nothing (an 8-byte-field object may round-trip to the same footprint), and identity hashCode interplay is implementation detail — do not quote "every object shrinks 8 bytes". Also: 519 made the feature a **product feature, not the default** — the JEP explicitly disclaims defaulting, which is a separate future step (JEP 534); the flag stays opt-in on 25 ([[What is Metaspace and how does it differ from PermGen]] is the other class-metadata card).

> [!tip] Interview answer
> **Compact object headers are Project Lilliput: experimental in 24, product in 25 — the 96-bit header (mark word plus compressed class pointer) becomes one 64-bit word with the class pointer folded in, typically saving eight bytes per object and improving density and cache locality. I keep it honest: savings vary with alignment, and identity hash plus lock state still live in that word.**
