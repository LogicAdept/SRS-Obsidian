<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is a stop the world pause in garbage collection and why do collectors minimize it?

> [!abstract] Short answer
> **A stop-the-world pause is an interval in which every application thread is halted and garbage collector threads run alone, so the heap view stays consistent while the collector works.** Classic Serial and Parallel collectors stop the world for whole collections; concurrent collectors stop it only for short root-oriented phases — G1's Remark and Cleanup, ZGC's root scanning. Pause goals stay soft: the guide promises G1 can "meet a pause-time goal with high probability", not guarantee one.

## What stops, what keeps running, and why

During a stop-the-world pause the application's threads — the **mutators** that allocate and update references — are all suspended; the collector's threads then trace, copy, sweep, or compact without anything changing under them. The reason is consistency: a tracer that starts from **GC roots** needs every root and every object field frozen while it decides what is live ([[What structures does the garbage collector analyze to find garbage]], [[How does the garbage collector decide an object can be collected]]). The tuning guide frames the whole topic this way: general collector features "are described in the context of the serial, stop-the-world collector" — full-stop collection is the baseline every other HotSpot collector relaxes.

| Collector (Java 21) | Stop-the-world profile |
| --- | --- |
| **Serial** | One GC thread; entire collections are full pauses |
| **Parallel** | Many GC threads; entire collections are full pauses, but shorter |
| **G1** | Young collections stop the world; marking runs concurrently with "two special stop-the-world pauses: Remark and Cleanup" |
| **ZGC** | "Stop-the-world phases are limited to root scanning" (JEP 333) — around a millisecond |
| **Shenandoah** | Pauses "long enough to scan the thread stacks" for roots; marking and compaction run concurrently |

## The metrics that make pauses matter

The guide names the two primary measures of garbage collection: "**Throughput** is the percentage of total time not spent in garbage collection considered over long periods of time" and "**Latency** is the responsiveness of an application. Garbage collection pauses affect the responsiveness of applications." Stop-the-world pauses are exactly where those two goals collide: a throughput-oriented collector accepts longer pauses to finish sooner overall, while latency-oriented collectors spend concurrent CPU to shrink each pause. The guide's scaling warning explains why this is not cosmetic — an application spending a seemingly trivial 1% of time in garbage collection on one processor "translates to more than a 20% loss in throughput on systems with 32 processors" (Amdahl's law applied to collector overhead).

```java
// Pause entries are first-class log lines in the unified GC log:
//   java -XX:+UseG1GC -Xlog:gc -Xmx64m StwDemo
//
//   GC(0) Pause Young (Normal) 46M->2M(64M) 2.4ms   <- app threads halted 2.4 ms
//   GC(1) Pause Young (Concurrent Start) 48M->3M(64M) 2.9ms
//   GC(2) Pause Remark 3M->3M(64M) 1.1ms            <- G1's special STW marking pause
//   GC(3) Pause Cleanup 1M->1M(64M) 0.4ms
class StwDemo {
    public static void main(String[] args) {
        for (int i = 0; i < 20; i++) {
            byte[] churn = new byte[2 * 1024 * 1024];
            java.util.Objects.requireNonNull(churn);
        }
        System.out.println("done");
    }
}
```

**Listing 1.** Every `Pause ...` line is a stop-the-world interval with its duration; even the concurrent G1 cycle shows STW anchors such as Remark and Cleanup between its concurrent phases. Line shapes vary by collector and release.

```d2
direction: down
run: "Mutators run\n(allocate, update fields)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
pause: "STW pause\nall mutators blocked" {
  width: 280
  height: 55
  style.fill: "#ffebee"
}
work: "GC threads work alone\ntrace, copy, sweep, compact" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
conc: "Concurrent phases\nGC works beside running mutators" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
run -> pause: "collection starts"
pause -> work
work -> conc: "concurrent collector:\nonly short pauses remain"
```

**Fig. 1.** A stop-the-world pause freezes mutators so collector threads see a consistent heap; concurrent collectors shrink but do not eliminate the red block.

> [!warning] "Concurrent" does not mean "no pauses"
> ZGC's promise is "without stopping the execution of application threads for more than a millisecond" — a millisecond pause is still a stop-the-world pause, just a tiny one rooted in root scanning rather than in the whole live set. Treating ZGC or Shenandoah as pause-free, or quoting `MaxGCPauseMillis` as a hard cap instead of a soft goal, fails the interview.

> [!warning] The spec does not even require pauses — or a collector design
> JVMS 2.5.3 says only that "heap storage for objects is reclaimed by an automatic storage management system (known as a garbage collector)" and that the JVM "assumes no particular type of automatic storage management system". Stop-the-world behavior, safepoints, and pause budgets are HotSpot implementation choices, not language promises.

> [!tip] Interview answer
> **A stop-the-world pause suspends all application threads so collector threads can run against a consistent heap view.** Serial and Parallel collect entirely inside such pauses; G1 stops for young collections plus Remark and Cleanup around concurrent marking; ZGC and Shenandoah limit pauses to root scanning and run tracing and relocation concurrently. Collectors minimize pauses because pauses are the latency term of the throughput-latency trade the guide defines — and because pause cost scales badly on many-core machines.

Related: [[What is Parallel GC]], [[What is G1 GC]], [[What is ZGC]], [[What is Shenandoah GC]], [[What are Minor GC and Full GC]], [[How would you explain tuning garbage collector settings on the JVM]]
