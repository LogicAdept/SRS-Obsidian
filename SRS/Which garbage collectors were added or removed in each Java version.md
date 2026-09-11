<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# Which garbage collectors were added or removed in each Java version

> [!abstract] Short answer
> **Serial and Parallel are the originals; CMS was introduced long ago, deprecated in 9 (JEP 291) and removed in 14 (363); G1 shipped experimental in 7, became the default in 9 (248) and stays default; ZGC arrived experimental in 11 (333), production in 15 (377), generational in 21 (439), default in 23 (474) with the non-generational mode removed in 24 (490); Shenandoah came experimental in 12 (189), production in 15 (379), generational in 25 (521); Epsilon, the no-op collector, landed in 11 (318); the GC interface that made all this pluggable is Java 10 (304).**

## The two arcs: the default and the latency specialists

G1's promotion in 9 (248) replaced CMS's generational-concurrent model with region-based evacuation and predictable pause targets; CMS removal in 14 (363) closed the chapter, and even the PS+SerialOld combo was deprecated in 14 (366). The latency specialists took a longer path: ZGC (colored pointers, sub-millisecond pauses, terabyte heaps) from experimental 11 through production 15 to generational-by-default 23; Shenandoah (forwarding pointers, Red Hat lineage, absent from Oracle builds) parallel to it, generational only in 25 (521, experimental 404 in 24). Epsilon (318) is the boundary case: a collector that allocates and never collects — useful for benchmarking and short-lived jobs. Collector availability is a vendor property: this deck's probe on Temurin 21 rejects `-XX:+UseEpsilonGC` even with `UnlockExperimentalVMOptions`, while accepting ZGC and Shenandoah flags ([[What is ZGC]], [[What is Shenandoah GC]]).

```java
import java.lang.management.ManagementFactory;
import java.util.List;

public class V39_GcTimeline {
    public static void main(String[] args) throws Exception {
        ManagementFactory.getGarbageCollectorMXBeans()
                .forEach(b -> System.out.println("active collector: " + b.getName()));
        var jdk = System.getProperty("java.home") + "/bin/java";
        for (String flag : new String[]{"-XX:+UseConcMarkSweepGC", "-XX:+UseG1GC",
                                        "-XX:+UseZGC", "-XX:+UseShenandoahGC",
                                        "-XX:+UseEpsilonGC", "-XX:+UseParallelGC",
                                        "-XX:+UnlockExperimentalVMOptions", "-XX:+UseEpsilonGC"}) {
            var p = new ProcessBuilder(List.of(jdk, flag, "-version")).redirectErrorStream(true).start();
            boolean ok = p.waitFor() == 0;
            new String(p.getInputStream().readAllBytes());
            System.out.println(flag + " -> " + (ok ? "ACCEPTED" : "REJECTED"));
        }
    }
}
```

**Listing 1.** Verified on Temurin JDK 21.0.12.1 (V39_GcTimeline in empirics): active collectors `G1 Young Generation`, `G1 Concurrent GC`, `G1 Old Generation`; `UseConcMarkSweepGC -> REJECTED` (removed in 14), `UseG1GC/UseZGC/UseShenandoahGC/UseParallelGC -> ACCEPTED`, `UseEpsilonGC -> REJECTED` even after `UnlockExperimentalVMOptions` — vendor builds may omit collectors entirely (out/V39_GcTimeline.txt).

```d2
direction: right
cms: "CMS\n9: deprecated (291)\n14: REMOVED (363)" { style.fill: "#ffebee"; width: 210; height: 100 }
g1: "G1\n9: DEFAULT (248)\n22: region pinning (423)\n26: throughput (522)" { style.fill: "#e8f5e9"; width: 230; height: 130 }
zgc: "ZGC\n11: experimental (333)\n15: production (377)\n21: generational (439)\n23: default (474)\n24: non-gen removed (490)" { style.fill: "#e3f2fd"; width: 240; height: 170 }
shen: "Shenandoah\n12: experimental (189)\n15: production (379)\n24: gen experimental (404)\n25: generational (521)" { style.fill: "#e3f2fd"; width: 240; height: 140 }
eps: "Epsilon\n11: experimental (318)\nno-op collector" { style.fill: "#fff3e0"; width: 220; height: 100 }
cms -> g1 -> zgc -> shen -> eps: ""
```

**Fig. 1.** Collector lifecycle by release: the default column (G1) evolves in place, the latency specialists climb from experimental to production to generational, CMS exits.

> [!warning] "Default" and "available" are per-vendor facts
> G1 has been the default since 9 across HotSpot builds, but Shenandoah never shipped in Oracle JDK, and Epsilon is missing from some vendor builds. Claims like "Java has four collectors" conflate the product with the spec — the supported set is whatever your build actually starts with ([[What is the default garbage collector by Java version]], [[Which garbage collectors in HotSpot]]).

> [!tip] Interview answer
> **The timeline: G1 became the default in 9 and CMS was deprecated the same release, removed in 14. ZGC entered at 11, went production in 15, generational in 21, default in 23. Shenandoah came at 12, production at 15, generational at 25. Epsilon landed in 11. The GC interface from 10 is what made collector pluggability real. I always add that availability is vendor-specific.**
