<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is the Epsilon garbage collector and when does a no-op collector make sense?

> [!abstract] Short answer
> **Epsilon (JEP 318, experimental since JDK 11, `-XX:+UseEpsilonGC`) is a fully passive collector: it allocates but never reclaims — when the heap is exhausted, "the JVM will shut down."** The JEP's summary: "Develop a GC that handles memory allocation but does not implement any actual memory reclamation mechanism." Its five use cases are all testing, measurement, or short-lived-job scenarios where a real collection cycle is waste.

## What a no-op collector actually does

Epsilon is a real HotSpot collector in every mechanical sense except reclamation. It "looks and feels like any other OpenJDK GC" behind its flag, implements "linear allocation in a single contiguous chunk of allocated memory", and issues **TLABs** — thread-local allocation buffers — with "trivial lock-free" code, so per-thread allocation stays as fast as the VM's normal path; humongous and out-of-TLAB allocations go through the same scheme. What it drops is everything that makes a collector a collector: "the barrier set used by Epsilon is completely empty/no-op, because the GC does not do any GC cycles, and therefore does not care about the object graph, object marking, object copying." The JEP's goal is "a completely passive GC implementation with a bounded allocation limit and the lowest latency overhead possible, at the expense of memory footprint and memory throughput", and its non-goals rule out reading it as manual memory management: "it is not a goal to introduce manual memory management features to Java language and/or JVM" ([[How does object memory allocation work]]).

## The five official use cases

| Use case | Why no-op wins |
| --- | --- |
| **Performance testing** | Differential analysis of real GCs with GC-induced artifacts filtered out — no worker scheduling, no barrier cost, no cycles "triggered at unfortunate times"; also estimates the natural latency baseline for low-latency work |
| **Memory pressure testing** | A bounded allocator that "fails on heap exhaustion" turns a memory invariant into a test: configure `-Xmx1g`, and the test crashes with a heap dump if the code allocates more |
| **VM interface testing** | Proves the minimum VM-GC interface is sane — a functional allocator with nothing implemented, valuable in light of JEP 304's Garbage Collector Interface |
| **Extremely short-lived jobs** | A job that exits quickly frees the heap anyway; "accepting the GC cycle to futilely clean up the heap is a waste of time" |
| **Last-drop latency and throughput** | For garbage-free or near-garbage-free ultra-latency-sensitive apps: no cycles ever; and since "the choice of GC means choosing the set of GC barriers", an empty barrier set removes even the write-barrier tax other collectors pay |

That last row is a real distinction from JEP 318: all mainline OpenJDK collectors "emit at least one reference write barrier" because they are generational (Shenandoah and ZGC being the non-generational exceptions of the era), while Epsilon's barrier set is empty ([[What is ZGC]], [[What is Shenandoah GC]]).

```java
// Epsilon in action — allocation succeeds until the heap is gone:
//   java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -Xmx64m EpsilonDemo
//
//   Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
//       ... JVM exits; no GC cycle ever ran
class EpsilonDemo {
    public static void main(String[] args) {
        java.util.List<byte[]> keep = new java.util.ArrayList<>();
        while (true) {
            keep.add(new byte[1024 * 1024]); // nothing ever reclaims these
        }
    }
}
```

**Listing 1.** Under Epsilon the loop ends in `OutOfMemoryError` once 64 MB is allocated — the JVM "shuts down" per the JEP summary instead of collecting. The experimental unlock is still required for this flag.

```d2
direction: right
a1: "Real collector:\nallocate -> GC -> reuse" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
a2: "Epsilon:\nallocate -> allocate -> ..." {
  width: 290
  height: 55
  style.fill: "#fff8e1"
}
oom: "Heap exhausted:\nOutOfMemoryError, exit" {
  width: 300
  height: 55
  style.fill: "#ffebee"
}
use: "Use cases: perf and memory\npressure testing, short jobs" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
a1 -> a2
a2 -> oom
oom -> use
```

**Fig. 1.** Every other collector closes the allocation loop with reclamation; Epsilon runs the loop open until the heap ends — and that failing-fast behavior is precisely its feature set.

> [!warning] Epsilon is not "System.gc disabled" and not a memory tool
> Disabling explicit calls still leaves a full collector running; Epsilon has no collector at all — no cycles, no barriers, no reclamation path. It is also not manual memory management: the JEP's non-goals explicitly reject that. Using it for a workload that outlives the heap is a misconfiguration, not tuning.

> [!warning] Experimental status and the barrier footnote
> JEP 318 delivered Epsilon as experimental in JDK 11 and it stays behind `-XX:+UseEpsilonGC` with the experimental unlock — do not present it as a production default candidate; the supported Java 21 catalog is Serial, Parallel, G1, ZGC. The no-barrier throughput claim applies to garbage-free workloads; a workload that actually allocates just hits the wall sooner ([[Which garbage collectors in HotSpot]]).

> [!tip] Interview answer
> **Epsilon is HotSpot's no-op collector (JEP 318, JDK 11, `UseEpsilonGC`): it allocates linearly through TLABs, has an empty barrier set, never reclaims, and brings the JVM down with OutOfMemoryError once the heap is exhausted.** Its use cases are performance testing, memory-pressure testing, VM-interface testing, extremely short-lived jobs, and last-drop latency or throughput for garbage-free applications — everywhere a real collection cycle would be pure waste.

Related: [[Which garbage collectors were added or removed in each Java version]], [[What was new in Java 11]], [[What is the default garbage collector by Java version]], [[How does object memory allocation work]]
