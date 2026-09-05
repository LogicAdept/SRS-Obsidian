<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How does garbage collection work on the JVM?

> [!abstract] Short answer
> **HotSpot traces from GC roots and reclaims objects no live thread can reach.** It is generational: most objects die in a young collection (copying survivors out of eden); longer-lived objects are promoted and collected less often. On Java 21 the usual default collector is G1 (region-based, pause-time *goal*). Parallel, Serial, and ZGC are the other collectors in the Oracle 21 catalog.

## Tracing, then generations

The VM never offers `free`. An object is garbage when it is **unreachable**: no path from a GC root (a live thread, statics of a reachable loader, JVM internals). HotSpot collectors are **tracing** — they identify reachable objects and reclaim the rest. A cycle of objects with no root path is still garbage ([[How does garbage collection treat cyclic references between live objects]], [[How does the garbage collector decide an object can be collected]]).

Walking the whole live set on every collection would scale with *live* data, which is expensive. HotSpot therefore uses **generational** collection under the weak generational hypothesis: most objects die young. The heap is split into pools by age:

- **Young generation** — almost all new objects are allocated in **eden**. A **minor** collection runs when the young generation fills; only that generation is collected. Live objects are **copied** from eden and one survivor space into the other survivor space. After a number of copies (aging), survivors are **promoted** into the old generation. A young generation full of dead objects is cheap: cost tracks live objects copied, not the garbage left behind.
- **Old generation** — objects that survived long enough. When it fills, a **major** collection typically covers the whole heap and lasts longer. Parallel can compact the old generation only as a whole. G1 instead reclaims old regions incrementally (mixed collections) and falls back to a full in-place heap compaction if it runs out of memory while marking.

Throughput is time *not* spent in GC. Latency is pause time. A huge young generation raises throughput and pause length; a small one does the opposite.

```d2
direction: right
eden: "Eden\n(new objects)" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
surv: "Survivor\n(copy / age)" {
  width: 160
  height: 70
  style.fill: "#fff8e1"
}
old: "Old\n(promoted)" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
eden -> surv: "minor GC"
surv -> surv: "copy until aged"
surv -> old: "promote"
```

**Fig. 1.** Serial-style young layout: allocate in eden, copy live objects through survivors, promote into old. G1 uses the same generations as noncontiguous **regions**.

## Which collector does that work (Java 21)

Let the VM pick unless you have a pause or throughput goal. Then:

| Collector | Role (HotSpot 21) |
| --- | --- |
| **G1** (`-XX:+UseG1GC`) | Usual default. Heap split into equal regions (eden / survivor / old / humongous). Generational, mostly concurrent marking, evacuating (copying) collections, pause-time *goal* with high probability — not a real-time SLA. Targeted at large heaps with a few-hundred-millisecond pause budget. |
| **Parallel** (`-XX:+UseParallelGC`) | Throughput collector: same generational idea as Serial, **multiple GC threads**. Was the default on server configurations before JDK 9 (JEP 248). Prefer when peak throughput matters and pauses of a second or longer are acceptable. |
| **Serial** (`-XX:+UseSerialGC`) | **One** GC thread. Small heaps (~100 MB) or single-processor boxes; still the ergonomic default on some constrained configurations. |
| **ZGC** (`-XX:+UseZGC`) | Concurrent, pause times under a millisecond and independent of heap size; heaps from a few hundred MB to 16 TB; some throughput cost. In 21, **generational** mode is `-XX:+ZGenerational` (JEP 439); plain `-XX:+UseZGC` is still the older non-generational collector that re-scans all objects. |

CMS (`-XX:+UseConcMarkSweepGC`) was deprecated in JDK 9 (JEP 291) and **removed** in JDK 14 (JEP 363). Asking for it on a current VM is ignored and you get the default collector.

```text
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 YourApp
java -XX:+UseParallelGC YourApp
java -XX:+UseZGC -XX:+ZGenerational YourApp
```

**Listing 1.** Collector choice is a launch flag. `MaxGCPauseMillis` is a G1 **soft** goal (default 200 ms), not a guarantee ([[Can developers control garbage collection or JVM memory settings]], [[What is G1 GC]], [[What are garbage collector generations]]).

G1’s cycle: **young-only** collections promote into old; when old occupancy hits the initiating threshold, concurrent marking starts; then **mixed** collections evacuate selected old regions that are mostly garbage (garbage-first). Live objects in the collection set are copied to new regions; empty source regions are reused. That is how G1 both copies and compacts without treating “mark-sweep-compact” as a separate old-gen collector.

> [!warning] “No references” is not the rule
> Reachability is from **roots**, not “the object still has a field pointing at something.” Two objects that only point at each other, with no root path, are garbage. A static cache that still points into the graph is not.

> [!warning] G1’s pause number is a goal
> `-XX:MaxGCPauseMillis` does not cap every pause. G1 is not a real-time collector. Full GC (in-place compaction) can still be very slow if the live set does not fit the evacuation plan.

> [!tip] Interview answer
> **The JVM traces from roots and frees unreachable objects; it does not wait for a cycle to “break.”** HotSpot is generational: copy quickly in young, promote survivors, collect old less often. On Java 21 you usually get G1; pick Parallel for throughput or ZGC when pauses must stay around a millisecond. CMS is gone.
