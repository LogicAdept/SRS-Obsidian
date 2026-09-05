<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How would you explain major garbage collector algorithms on the JVM?

> [!abstract] Short answer
> **HotSpot collectors all *trace* reachable objects; they differ in *when* they stop the world and *how* they compact.** Young collections **copy** (evacuate) survivors. Old space is either compacted as a whole (Parallel), evacuated a few regions at a time (G1), or relocated concurrently (ZGC). CMS was concurrent mark-sweep and is gone. There is no single “old gen = mark-sweep-compact” algorithm on modern HotSpot.

## Tracing first, then how space is reclaimed

Every HotSpot collector is a **tracing** collector: it finds objects reachable from GC roots and treats the rest as garbage ([[How does the garbage collector decide an object can be collected]]). Naive tracing of the whole live set every time is expensive, so most collectors are also **generational**: copy quickly in young, visit old less often ([[How does garbage collection work on the JVM]], [[What are garbage collector generations]]).

How live objects are *moved* is the algorithm people mean by copying / compact / concurrent:

| Move / reclaim style | Where you see it (Java 21) |
| --- | --- |
| **Copying / evacuation** | Young generation in Serial and Parallel: live objects in eden and one survivor space are **copied** into the other survivor space; the source spaces are then empty. G1 does the same idea per **region**: live objects in the collection set are copied to new regions, which **compacts** as a side effect (garbage-first: emptiest regions first). |
| **Whole-heap compact** | Parallel can compact and reclaim the **old generation only as a whole** — one long pause. G1’s backup Full GC is an in-place stop-the-world compact of the entire heap. |
| **Mostly concurrent mark + incremental evacuate** | G1: concurrent marking of old, then **mixed** collections that evacuate selected old regions while still doing young work. Pause-time *goal*, not real-time. |
| **Concurrent relocate** | ZGC: almost all work beside the application; pauses typically under a millisecond and independent of heap size. **Colored pointers** plus **load barriers** (and **store barriers** in generational mode) keep the mutator’s view consistent while objects move. Java 21: `-XX:+UseZGC -XX:+ZGenerational` for young/old collected independently (JEP 439). |
| **Concurrent mark-sweep (historical)** | CMS: two STW pauses (initial mark, remark) around concurrent tracing. **Removed** in JDK 14 (deprecated JDK 9). It did *not* compact like Parallel/G1; that is why “CMS old gen” is the wrong template for G1/ZGC. |

Serial is the same generational copy/promote story as Parallel, but **one** GC thread. Parallel uses **many** GC threads for throughput. Neither is “copying in young and mark-sweep-compact as a separate named old-gen collector” in the Java 21 guide — the documented old-gen contrast is **compact the old generation as a whole** versus G1’s incremental evacuation ([[What is Serial GC]], [[What is Parallel GC]], [[What is G1 GC]], [[What is ZGC]], [[What is CMS Concurrent Mark Sweep GC]]).

```d2
direction: down
trace: "Trace from roots" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
copy: "Copy / evacuate\n(young, G1 regions)" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
compact: "Compact old as a whole\n(Parallel; G1 Full GC)" {
  width: 260
  height: 55
}
conc: "Concurrent mark / relocate\n(G1 mark, ZGC)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
trace -> copy
trace -> compact
trace -> conc
```

**Fig. 1.** Shared predicate (reachability). Split on whether you copy a nursery, compact all of old in one pause, or mark/relocate beside the mutator.

```text
# Throughput: parallel compact of old as a whole
java -XX:+UseParallelGC YourApp

# Incremental evacuate + concurrent mark (default)
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 YourApp

# Concurrent relocate; generational in 21 is opt-in
java -XX:+UseZGC -XX:+ZGenerational YourApp
```

**Listing 1.** Algorithm choice is the collector flag. `MaxGCPauseMillis` is a G1 **goal**. In 21, ZGC is generational only with `+ZGenerational`.

> [!warning] Old generation is not “mark-sweep-compact” by default
> Copying in **young** is real. Treating every old generation as Mark → Sweep → Compact describes neither G1 (regional evacuate) nor ZGC (concurrent relocate) nor CMS (mark-sweep **without** that compact story). Parallel’s documented old-gen move is compact **as a whole**.

> [!warning] Concurrent is not “no pauses”
> G1 still stops the world for evacuation. CMS had initial-mark and remark pauses. ZGC aims at sub-millisecond pauses, not zero. Shenandoah is not in the Oracle Java 21 collector catalog; do not pair it with ZGC as if both were documented there.

> [!tip] Interview answer
> **They all trace; young GCs copy survivors; they differ in how they compact old.** Parallel compactes old in one pause. G1 evacuates garbage-first regions and marks concurrently. ZGC relocates with colored pointers and tiny pauses. CMS was concurrent mark-sweep and was removed in 14 — do not recite mark-sweep-compact as the one old-gen algorithm.
