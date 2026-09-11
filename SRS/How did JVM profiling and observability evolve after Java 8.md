<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# How did JVM profiling and observability evolve after Java 8

> [!abstract] Short answer
> **Java 11 open-sourced Flight Recorder (JEP 328) and added low-overhead heap profiling (331); 14 added JFR event streaming for in-process live reads (349); 21 added `jcmd JFR.view` aggregations; 25 added CPU-time profiling (509), cooperative sampling (518), and method timing & tracing (520). On the removal side, 9 deleted the hprof agent (240) and jhat (241), pushing profiling onto JFR-based tooling.**

## The JFR-centric arc

Before 11, JFR was a commercial Oracle JDK feature — OpenJDK users had no supported flight-recorder path. Open-sourcing it (328, with Mission Control unbundled) made event-based, low-overhead, always-on profiling the platform default answer, and 331 added stack-sampled allocation events without full-heap walking. JFR event streaming (349) flipped the consumption model: the running process can read its own recording via the `jdk.jfr` API — dashboards and adaptive behavior no longer parse files post-mortem. The 25 batch modernizes sampling itself: CPU-time-based profiling (clock-aware, not wall-time), cooperative sampling to cut safepoint bias, and method timing/tracing events ([[What is profiling in Java]], [[How do you capture a Java heap dump]]).

```java
import jdk.jfr.Recording;
import jdk.jfr.consumer.RecordingFile;

import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

public class V53_JfrEvolution {
    public static void main(String[] args) throws Exception {
        Path file = Files.createTempFile("jfr-demo", ".jfr");
        Recording r = new Recording();                     // jdk.jfr: open-sourced in 11 (JEP 328)
        r.enable("jdk.CPULoad").withPeriod(Duration.ofMillis(50));
        r.start();
        long start = System.nanoTime();
        double x = 0;
        while (System.nanoTime() - start < 300_000_000L) { x += Math.sqrt(x + 1); }
        r.stop();
        r.dump(file);
        long events = RecordingFile.readAllEvents(file).stream()
                .filter(e -> e.getEventType().getName().equals("jdk.CPULoad")).count();
        System.out.println("cpu-load events captured=" + (events > 0) + " (work=" + (x != 0) + ")");
        r.close();
    }
}
```

**Listing 1.** Verified on JDK 21 (V53_JfrEvolution in empirics): `cpu-load events captured=true (work=true)` (out/V53_JfrEvolution.txt) — programmatic recording and reading inside the same process, the 328+349 capability pair on 21.

```d2
direction: right
j11: "JDK 11\nJFR open-sourced (328)\nheap profiling (331)" { style.fill: "#e8f5e9"; width: 240; height: 90 }
j14: "JDK 14\nJFR event streaming (349)\nin-process live reads" { style.fill: "#e3f2fd"; width: 260; height: 90 }
j21: "JDK 21\njcmd JFR.view aggregations" { style.fill: "#e3f2fd"; width: 250; height: 90 }
j25: "JDK 25\nCPU-time profiling (509),\ncooperative sampling (518),\nmethod timing (520)" { style.fill: "#e8f5e9"; width: 300; height: 120 }
j11 -> j14 -> j21 -> j25: ""
```

**Fig. 1.** Observability since 8: JFR becomes free, then streamable, then aggregated, then sampling-aware.

> [!warning] "Free JFR" is an 11 fact, not an 8 fact
> On Oracle JDK 8, JFR required a commercial license; answering "we always had JFR" flattens a licensing boundary that shaped tooling choices. Also the old `hprof` heap-dump agent died in 9 — class-name-based heap profiling answers built on it are obsolete ([[What was new in Java 11]]).

> [!tip] Interview answer
> **The arc is JFR-centric: 11 open-sourced Flight Recorder with low-overhead allocation events, 14 added event streaming so the process reads its own recording live, 21 gave jcmd JFR.view aggregates, and 25 upgraded sampling itself with CPU-time profiling, cooperative sampling, and method timing. Meanwhile hprof and jhat left in 9, consolidating everything on JFR tooling.**
