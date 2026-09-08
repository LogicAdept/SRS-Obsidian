<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# Which garbage collectors in HotSpot?

> [!abstract] Short answer
> The Java 21 GC Tuning Guide catalogs **four** HotSpot collectors, selected by flags: **Serial** (`-XX:+UseSerialGC`) — one thread, best for small heaps (up to ~100 MB) or single processors; **Parallel**, the "throughput collector" (`-XX:+UseParallelGC`) — multiple GC threads, for peak throughput when pauses of a second or longer are acceptable; **G1** (`-XX:+UseG1GC`) — a "mostly concurrent", region-based collector that "is selected by default on most hardware and operating system configurations" and targets a **pause-time goal**; and **ZGC** (`-XX:+UseZGC`, with `-XX:+ZGenerational` for the generational mode) — "max pause times **under a millisecond**, but at the cost of some throughput", pause-independent of heap size up to **16 TB**. **CMS no longer exists** — "Remove the Concurrent Mark Sweep (CMS) garbage collector" (JEP 363, JDK 14); **G1 became the default in JDK 9** (JEP 248). Ergonomics choose G1 on **server-class machines** and Serial otherwise. Event vocabulary: [[What are Minor GC and Full GC]]; tuning knobs: [[Can developers control garbage collection or JVM memory settings]].

## The four, in their own words

The Tuning Guide characterizes each collector; the distinctions are thread count, pause model, and target workload:

* **Serial** — "uses a **single thread** to perform all garbage collection work, which makes it relatively efficient because there is no communication overhead between threads. It's best-suited to **single processor machines** ... although it can be useful on multiprocessors for applications with **small data sets (up to approximately 100 MB)**."
* **Parallel** — "also known as **throughput collector** ... has multiple threads that are used to speed up garbage collection ... intended for applications with medium-sized to large-sized data sets that are run on **multiprocessor** or multithreaded hardware."
* **G1** — "a **mostly concurrent** collector ... designed to scale from small machines to large multiprocessor machines with a large amount of memory. It provides the capability to meet a **pause-time goal** with high probability, while achieving high throughput." Internally: "G1 partitions the heap into a set of **equally sized heap regions**"; it is "a generational, incremental, parallel, mostly concurrent, stop-the-world, and **evacuating** garbage collector."
* **ZGC** — "provides **max pause times under a millisecond**, but at the cost of some throughput ... Pause times are **independent of heap size** that is being used. ZGC works well for heap sizes from a few hundred megabytes to **16TB**."

The algorithm deep-dive for the classic pair is in [[How does the Serial GC work]]; G1's region mechanics are sketched in [[How does garbage collection work on the JVM]].

```java
// Selecting and verifying a collector on the java command line (Java 21):
//
//   java -XX:+UseSerialGC   -Xlog:gc -version   // single-threaded
//   java -XX:+UseParallelGC -Xlog:gc -version   // throughput collector
//   java -XX:+UseG1GC       -Xlog:gc -version   // default on most hardware
//   java -XX:+UseZGC -XX:+ZGenerational -Xlog:gc -version  // sub-ms pauses
//
// -Xlog:gc prints the active collector and every pause;
// -XX:+PrintFlagsFinal -version | grep UseG1GC confirms the resolved flag.
class CollectorProbe {
    public static void main(String[] args) {
        System.out.println("Collector check: see the -Xlog:gc output above.");
    }
}
```

**Listing 1.** Every collector is a command-line flag; `-Xlog:gc` (Unified Logging, Java 21) makes the choice and the pauses visible.

```d2
direction: right
start: "What matters first?" {style.fill: "#e3f2fd"}
throughput: "peak throughput,\npauses OK >= 1s" {style.fill: "#fff8e1"}
pause: "bounded pauses,\nservers" {style.fill: "#e8f5e9"}
ultra: "sub-millisecond\nlatency" {style.fill: "#e8f5e9"}
small: "small heap ~100 MB\nor 1 CPU" {style.fill: "#ffebee"}
parallel: "Parallel\n-XX:+UseParallelGC" {style.fill: "#fff8e1"}
g1: "G1 (default)\n-XX:+UseG1GC" {style.fill: "#e8f5e9"}
zgc: "ZGC\n-XX:+UseZGC" {style.fill: "#e8f5e9"}
serial: "Serial\n-XX:+UseSerialGC" {style.fill: "#ffebee"}
start -> throughput: "no pause goal"
start -> pause: "pause-time goal"
start -> ultra: "lowest latency"
start -> small: "tiny footprint"
throughput -> parallel
pause -> g1
ultra -> zgc
small -> serial
```

**Fig. 1.** The guide's own selection logic as a decision tree — start from your requirement, not from a collector's reputation.

## Defaults and history you are expected to know

Ergonomics pick the collector before any flag does: "Garbage-First (G1) Collector **on server-class machines**, Serial Collector otherwise", where a machine is server-class if "the VM detects **two or more processors** and physical memory larger than or equal to **1792 MB**". Heap defaults follow the same logic — "initial heap size of **1/64** of physical memory", "maximum heap size of **1/4** of physical memory". History in two sentences: **JDK 9** made G1 the default on server configurations (JEP 248); **JDK 14** removed CMS (JEP 363) after G1 was built to replace it. Since **JDK 21**, ZGC ships in a **generational** flavor (JEP 439): "The `-XX:+ZGenerational` option enables the new, Generational version of ZGC", while plain `-XX:+UseZGC` still selects the non-generational one.

> [!warning] Mentioning CMS as a current collector ends the interview
> Lists that start with "Serial, Parallel, **CMS**, G1" are quoting a pre-2019 source: CMS was deprecated in JDK 9 and **removed in JDK 14** — its flag `-XX:+UseConcMarkSweepGC` is gone from the Java 21 reference. Two adjacent traps: calling G1 "concurrent only" (it is *mostly* concurrent and its evacuation pauses are stop-the-world), and assuming ZGC is generational by default in 21 — in Java 21 generational ZGC is the **opt-in** `-XX:+ZGenerational` mode, not the default.

> [!tip] Interview answer
> **On Java 21 HotSpot ships four collectors: Serial for single-threaded small-heap cases, Parallel — the throughput collector — for jobs that tolerate second-scale pauses, G1, which is the default since JDK 9 and targets a pause-time goal with heap regions, and ZGC with sub-millisecond pauses independent of heap size, generational since the ZGenerational mode. CMS is gone — removed in JDK 14. Ergonomics default to G1 on server-class machines and Serial otherwise. The flag names — UseSerialGC, UseParallelGC, UseG1GC, UseZGC — are worth knowing cold.**
