<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What are Minor GC and Full GC?

> [!abstract] Short answer
> These are names for **collection events**, not separate programs. A **minor collection** runs when the **young generation fills up** and collects **only** the young generation: "When the young generation fills up, it causes a minor collection in which only the young generation is collected; garbage in other generations isn't reclaimed" (GC Tuning Guide). A **major collection** collects the **entire heap**: "Eventually, the old generation fills up and must be collected, resulting in a major collection, in which the entire heap is collected. Major collections usually last **much longer** than minor collections." **Full GC** is the HotSpot-log name for that whole-heap event. Both are **stop-the-world** in the classic collectors — the application's threads are suspended — which is why the weak generational hypothesis ("most objects survive for only a short period of time") is the whole design trick: young collections are cheap because most of the young generation is already dead. Collector catalogue: [[Which garbage collectors in HotSpot]]; generation layout: [[What are garbage collector generations]].

## Why minor collections are cheap

The cost of a tracing collection scales with the number of **live** objects, not the size of the region. A young generation "full of dead objects is collected very quickly" — the guide states the costs "are, to the first order, proportional to the number of live objects being collected". Since most objects die young, a minor collection copies the few survivors out (into a survivor space or straight to the old generation) and resets Eden. The pause is short — in the serial collector a single thread does it; in Parallel and G1, several threads split the work.

## Why major / Full GC is the alarm event

A major collection touches the **entire heap**, including the long-lived set the application is actively using, and in the classic collectors it compacts the old generation to keep allocation cheap afterwards. That combination makes it the longest pause a traditional collector produces. Frequent Full GCs therefore mean the old generation keeps filling up — survivors are being promoted faster than the old generation can absorb them, which is the classic signature of either a too-small heap or a leak. The guide's own guard rail quantifies "too much": "If more than **98%** of the total time is spent in garbage collection and less than **2%** of the heap is recovered, then an `OutOfMemoryError` is thrown" (documented for the parallel collector) — the VM refuses to spin forever at 100% GC. Diagnosis path: [[How do you diagnose memory pressure and OutOfMemoryError]].

```java
// -Xlog:gc           -> per-collection lines, e.g.:
//   GC(0) Pause Young (Normal) (G1 Evacuation Pause) 25M->3M(256M) 2.1ms
//   GC(12) Pause Full (G1 Compaction Pause) 246M->88M(256M) 41.7ms
// -Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=20m
//
// Reading the line: <heap before> -> <heap after>(<capacity>) <pause duration>.
// Young pauses short and frequent: healthy. Full pauses climbing in
// frequency and reclaiming less each time: leak investigation starts now.
class GcLogFacts {
    static long retainedTotal;
    static void retainAll(java.util.List<byte[]> buffers) {
        retainedTotal = buffers.stream().mapToLong(b -> b.length).sum();
        // buffers unreachable here -> young garbage, minor GC reclaims;
        // retainedTotal keeps only a number, not the arrays themselves.
    }
}
```

**Listing 1.** The `-Xlog:gc` output shape (Unified Logging, Java 21) and the allocation habit that keeps major collections rare: let objects die young, never pin them in statics.

```d2
direction: right
alloc: "app allocates\nin Eden" {style.fill: "#e3f2fd"}
young: "Eden fills" {style.fill: "#fff3e0"}
minor: "Minor GC\nyoung only, short pause" {style.fill: "#e8f5e9"}
promote: "survivors age,\npromoted to Old" {style.fill: "#fff8e1"}
old: "Old fills" {style.fill: "#ffebee"}
full: "Major / Full GC\nentire heap, long pause" {style.fill: "#b71c1c"}
oom: "98% time in GC +\n<2% reclaimed -> OOM" {style.fill: "#b71c1c"}
alloc -> young -> minor -> promote -> old -> full
full -> oom: "if GC-bound"
```

**Fig. 1.** The collection cycle: minor events are routine and cheap; a major event is the heap-wide one — and a GC-bound death spiral ends in `OutOfMemoryError` by design.

## Vocabulary the interview actually tests

Three distinctions collapse into one paragraph if you are careful. First, **minor vs major** is about *scope* (young only vs entire heap) and *duration*, not about different algorithms — the same tracing machinery runs at both scales. Second, **Full GC** is the log/event name; in casual speech "major" and "full" are used interchangeably, and even the guide's own sentence equates the two (a major collection collects the entire heap). Third, **stop-the-world** describes the pause model, not an event: every classic HotSpot collector suspends application threads for at least some phases; how much and how often is exactly what separates Serial from Parallel from G1 from ZGC. Modern concurrent collectors blur the edges — G1 runs most of its work concurrently but still pauses for evacuation, so its "Pause Young" lines are STW too.

> [!warning] "Major GC collects only the old generation" is imprecise
> The folk definition ("minor = young, major = old") is half-right and the guide is stricter: a major collection is declared when the old generation fills up but it collects the **entire heap**. Repeating the folk version with confidence — or claiming minor GC is "not stop-the-world" — costs credibility. The precise phrasing: minor touches only young; major/full is the whole-heap event, triggered by old-generation pressure; all classic HotSpot collectors pause the application for them, differing in thread count and concurrency of non-pause phases.

> [!tip] Interview answer
> **Minor GC collects only the young generation when Eden fills up — it's fast because cost scales with live objects and most objects die young per the weak generational hypothesis. Major — or Full GC in the logs — is the whole-heap event triggered when the old generation fills up, and it's the long pause in classic collectors. Both are stop-the-world in serial, parallel and G1; frequent Full GCs with shrinking reclamation is the leak signature, and HotSpot itself throws OutOfMemoryError past 98% time in GC with under 2% of heap recovered.**
