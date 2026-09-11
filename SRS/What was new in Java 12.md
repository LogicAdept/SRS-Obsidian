<!--
reps: 0
priority: 0
-->
#Java/Versions/12 #SRS

# What was new in Java 12

> [!abstract] Short answer
> **Java 12 (March 2019) previewed switch expressions (JEP 325) and shipped Shenandoah as an experimental collector (JEP 189), a JMH-based microbenchmark suite inside the JDK build (JEP 230), default CDS archives (JEP 341), JVM constants API (JEP 334), and two G1 upgrades: abortable mixed collections (JEP 344) and promptly returning unused committed memory (JEP 346). API odds: `Collectors.teeing`, `String.indent/transform`, compact `NumberFormat`.**

## Collector and library moves

Shenandoah (JEP 189) is a low-pause collector that compacts concurrently via forwarding pointers, distinct from G1 pause-based evacuation and from ZGC colored pointers. It matters as a version fact twice: experimental in 12, production in 15 (JEP 379), and notably absent from Oracle own JDK builds — other vendors shipped it. The G1 pair (344/346) targets the two classic G1 complaints: mixed collections that could not be aborted once started, and a heap that stayed fat after a demand spike (12 lets G1 give memory back to the OS; 13 did the same for ZGC, JEP 351).

```java
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class V28_Java12 {
    public static void main(String[] args) {
        String stats = Stream.of(3, 1, 4, 1, 5).collect(Collectors.teeing(   // JDK 12
                Collectors.counting(),
                Collectors.summingInt(Integer::intValue),
                (Long count, Integer sum) -> "count=" + count + " sum=" + sum
                        + " avg=" + (sum / (double) count)));
        System.out.println(stats);
        String reversed = "jdk12".transform(s -> new StringBuilder(s).reverse().toString()); // 12
        System.out.println(reversed);
        System.out.println("col1\nrow2".indent(2).replace(" ", "."));     // 12
    }
}
```

**Listing 1.** Verified on JDK 21 (V28_Java12 in empirics): `count=5 sum=14 avg=2.8`, `21kdj`, `..col1` / `..row2` (out/V28_Java12.txt). `teeing` runs two collectors over one stream and merges their results.

```d2
direction: right
preview: "switch expressions\nPREVIEW (325)" { style.fill: "#fff3e0"; width: 210; height: 80 }
gc: "Shenandoah EXPERIMENTAL (189)\nG1 abortable mixed (344)\nG1 returns memory (346)" { style.fill: "#e8f5e9"; width: 310; height: 100 }
tools: "Microbenchmark suite (230)\nDefault CDS (341)\nConstants API (334)" { style.fill: "#e3f2fd"; width: 290; height: 100 }
preview -> gc -> tools: ""
```

**Fig. 1.** Java 12 buckets: one famous preview, one experimental collector, and build/CDS/G1 groundwork.

> [!warning] Preview and experimental mean what they say
> Switch expressions in 12 required `--enable-preview` and changed slightly before finalizing in 14 ([[What are switch expressions]]). Shenandoah in 12 was experimental and missing from Oracle builds entirely — "we ran Shenandoah on Oracle JDK 12" was never a true statement; it ran on vendor builds like Temurin ([[Which garbage collectors were added or removed in each Java version]]).

> [!tip] Interview answer
> **Java 12 previewed switch expressions, shipped Shenandoah experimentally, and improved G1: abortable mixed collections plus returning unused memory to the OS (JEPs 344/346). It also added `Collectors.teeing`, `String.indent/transform`, default CDS archives, and a JMH microbenchmark suite in the JDK build. The sleeper fact: Oracle JDK never included Shenandoah.**
