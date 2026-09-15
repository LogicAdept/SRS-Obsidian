<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is the difference between parallel and concurrent garbage collection phases?

> [!abstract] Short answer
> **Parallel means many collector threads doing GC work together while application threads are stopped; concurrent means collector work overlapping the running application.** The tuning guide lists them as distinct HotSpot techniques: "use multiple threads to aggressively make operations parallel, or perform some long-running operations in the background concurrent to the application." A collector can be both — G1 marks concurrently and evacuates in parallel stop-the-world pauses.

## Two independent axes

Every HotSpot collector sits on two axes. The first is **thread count inside a collection**: Serial uses one GC thread; Parallel, G1, ZGC, and Shenandoah use many. The second is **application cooperation**: stop-the-world phases freeze all mutators; concurrent phases let mutators keep running while GC works beside them. Confusing the axes produces the classic wrong answers — "parallel" does not imply the application keeps running, and "concurrent" does not imply multiple GC threads working in parallel on the same phase. The guide's own wording separates them cleanly in one sentence: collectors "use multiple threads to aggressively make operations parallel, or perform some long-running operations in the background concurrent to the application" ([[What is Serial GC]], [[What is Parallel GC]]).

| Collector (Java 21) | Parallel phases | Concurrent phases |
| --- | --- | --- |
| **Serial** | none — one GC thread | none |
| **Parallel** | whole collections, many GC threads, full stop-the-world | none |
| **G1** | young and mixed evacuations (STW, many threads) | old-generation marking between Concurrent Start and Remark |
| **ZGC** | root-scanning pauses | "performs all expensive work concurrently" (guide) |
| **Shenandoah** | root scan and update pauses | "Shenandoah adds concurrent compaction" (project page) |

## What each axis buys and costs

Parallelism attacks the duration of a pause: "enabling the parallel collector should make the collection pauses shorter", because "multiple garbage collector threads are participating in a minor collection" (guide, Parallel chapter). The application still stops, but fewer cores are idle while it does. Concurrency attacks the pause itself: instead of concentrating work where the application is frozen, the collector moves long-running pieces — tracing (G1, ZGC, Shenandoah) and even relocation and compaction (ZGC, Shenandoah) — to run while mutators run. The price is explicit in the guide's G1 chapter: "G1 performs parts of its work at the same time as the application runs. It trades processor resources which would otherwise be available to the application for shorter collection pauses." Concurrency taxes throughput in CPU cycles and barrier overhead; parallelism taxes it only during pauses, which is why the guide's Amdahl discussion still matters: collector overhead that looks negligible on one core dominates scaling on 32.

In Java 21's Oracle catalog there are "four supported garbage collection alternatives" — Serial, Parallel, G1, ZGC — and "all but one of them, the serial GC, parallelize the work"; only G1, ZGC, and the OpenJDK builds' Shenandoah go further and make phases concurrent ([[What is G1 GC]], [[What is ZGC]], [[What is Shenandoah GC]]).

```java
// Same heap, three collectors, one log line each (unified GC log):
//   java -XX:+UseSerialGC  -Xlog:gc -Xmx64m AxesDemo
//     GC(0) Pause Young (Allocation Fail) 18M->2M(64M) 5.1ms      <- 1 thread, longer pause
//   java -XX:+UseParallelGC -Xlog:gc -Xmx64m AxesDemo
//     GC(0) Pause Young (Allocation Fail) 18M->2M(64M) 1.6ms      <- parallel STW, shorter pause
//   java -XX:+UseZGC        -Xlog:gc -Xmx64m AxesDemo
//     GC(0) Garbage Collection (Warmup) 18M->2M(64M) 2.2ms        <- mostly concurrent, no "Pause"
class AxesDemo {
    public static void main(String[] args) {
        for (int i = 0; i < 5; i++) {
            byte[] churn = new byte[4 * 1024 * 1024];
            java.util.Objects.requireNonNull(churn);
        }
        System.out.println("same workload, different axis");
    }
}
```

**Listing 1.** Serial and Parallel both show `Pause Young` — the difference is thread count, visible as the shorter duration; ZGC's cycle logs without a leading `Pause` because its work is concurrent. Durations are illustrative for a tiny heap.

```d2
direction: right
app1: "Mutators: stopped" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
par: "Parallel GC:\nmany GC threads" {
  width: 220
  height: 55
  style.fill: "#fff8e1"
}
app2: "Mutators: running" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
conc: "Concurrent GC:\n1+ GC threads beside app" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
app1 -> par
app2 -> conc
```

**Fig. 1.** Parallel = more GC threads inside a frozen world; concurrent = GC working while mutators run. G1 combines both: concurrent marking, parallel STW evacuation.

> [!warning] Both classic confusions fail
> "Parallel GC is concurrent because it has many threads" — false: Parallel is entirely stop-the-world; its parallelism is between GC threads, not between GC and application. "Concurrent collectors never stop the world" — equally false: G1 has young collections plus Remark and Cleanup, ZGC stops for root scanning, Shenandoah scans and updates roots in pauses ([[What is a stop the world pause in garbage collection and why do collectors minimize it]]).

> [!warning] Do not cross domains with the words
> "Parallel" in `java.util` (parallel streams) is application-level parallelism on ForkJoin pools — unrelated to collector thread counts. In GC vocabulary the words answer one question only: who else is running during GC work — other GC threads (parallel) or the application itself (concurrent).

> [!tip] Interview answer
> **Parallel means multiple GC threads cooperating on a stop-the-world phase; concurrent means the collector works while application threads keep running.** Serial is neither parallel nor concurrent; Parallel is parallel-only; G1 is both (concurrent marking, parallel STW evacuation); ZGC and Shenandoah push evacuation and compaction into concurrent work, keeping only millisecond-scale root pauses. Parallel buys shorter pauses, concurrency buys fewer and smaller pauses — both are paid in throughput.

Related: [[What is G1 GC]], [[What is ZGC]], [[What is Shenandoah GC]], [[What is the default garbage collector by Java version]], [[How would you explain major garbage collector algorithms on the JVM]]
