<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How does the Serial GC work?

> [!abstract] Short answer
> The Serial collector runs everything on **one thread** with full **stop-the-world** pauses, and it is the textbook algorithm the other generational collectors parallelize. **Young generation — copying:** "The young generation consists of **eden and two survivor spaces**. Most objects are initially allocated in eden. One survivor space is **empty at any time**, and serves as the destination of live objects in eden and the other survivor space during garbage collection; after garbage collection, eden and the source survivor space are empty. In the next garbage collection, the purpose of the two survivor spaces are exchanged" — objects bounce between survivors "until they've been copied a certain number of times or there isn't enough space left there", then go to the old generation ("this process is also called **aging**"). **Old generation — mark, sweep, compact:** live objects are marked from the roots, dead ones are reclaimed, and survivors slide to the start of the space so the guide's third technique applies — "recover **larger contiguous free memory** by compacting live objects." Catalogue context: [[Which garbage collectors in HotSpot]]; the event names: [[What are Minor GC and Full GC]].

## A minor collection, step by step

Start the steady state: Eden holds new objects, `From` survivor holds the previous round's survivors, `To` survivor is empty. The single GC thread then:

1. **Traces** from GC roots through Eden and `From`, marking everything reachable.
2. **Copies** young survivors into `To`; objects that have aged past the **tenuring threshold** are promoted **directly to the old generation** instead.
3. **Swaps** the survivor roles — the filled `To` becomes the new `From`, and Eden plus the old `From` come back completely empty.
4. **Handles overflow**: if `To` fills up before the trace finishes, the remaining survivors are promoted to the old generation regardless of age — they have nowhere else to go.

The scheme is called **copying collection**, and its price is structural: the young generation must always keep a survivor space empty, so it "wastes" part of the heap it manages. That trade is acceptable exactly because the young generation is small relative to the whole heap and full of dead objects — the weak generational hypothesis at work.

## The old generation: mark, sweep, compact

Copying stops making sense for the old generation — it is large and mostly *live*, so tracing-and-copying would churn long-lived data. Instead, a major collection runs in three phases: **mark** everything reachable from the roots; **sweep** away the unmarked; **compact** the survivors toward the beginning of the space, so the free memory becomes one contiguous block. The guide lists compaction among HotSpot's core techniques — "Try to recover larger contiguous free memory by **compacting live objects**" — because bump-the-pointer allocation into a contiguous region is far cheaper than hunting for holes in a fragmented space. This is the trade the old generation makes: slower individual collections, but simple, fast allocation between them.

```java
// Watching the Serial collector do exactly this (Java 21):
//   java -XX:+UseSerialGC -Xlog:gc,gc+heap=info -Xmx64m SerialGcDemo
//
// Expected log lines:
//   GC(0) Pause Young (Allocation Fail) 18M->2M(64M) 1.9ms   <- copying
//   GC(7) Pause Full (System.gc()) 41M->9M(64M) 6.8ms        <- mark-sweep-compact
class SerialGcDemo {
    public static void main(String[] args) {
        for (int round = 0; round < 5; round++) {
            byte[] churn = new byte[4 * 1024 * 1024]; // dies young -> Eden
            byte[] kept  = new byte[1024 * 1024];     // survives -> survivors -> Old
            java.util.Objects.requireNonNull(churn);
            java.util.Objects.requireNonNull(kept);
        }
        System.gc();                                  // forces a full, compacting pass
    }
}
```

**Listing 1.** Short-lived churn exercises the Eden/survivor copying; surviving allocations age into the old generation, and `System.gc()` exposes its mark-sweep-compact pass in the log.

```d2
direction: right
eden: "Eden\n(new objects)" {style.fill: "#e3f2fd"}
from: "From survivor\n(last round)" {style.fill: "#fff3e0"}
to: "To survivor\n(EMPTY)" {style.fill: "#ffebee"}
old: "Old generation\n(promoted, long-lived)" {style.fill: "#f0f0f0"}
eden -> to: "copy young survivors"
from -> to: "copy + age"
from -> old: "aged past threshold"
to -> from: "roles swap\neden empties"
old -> old: "major: mark, sweep,\ncompact to start" {style.stroke: "#b71c1c"}
```

**Fig. 1.** The serial generational cycle: copying inside the young generation with aging into Old, and a compacting mark-sweep for the whole heap when Old fills.

## Why learn this "slow" collector first

Serial is where every mechanism is visible without concurrency noise: one thread, two behaviors — scavenging with aging for the young, mark-sweep-compact for the old — and explicit stop-the-world boundaries. Parallel is the same algorithms with **more threads** ("The primary difference between the serial and parallel collectors is that the parallel collector has multiple threads that are used to speed up garbage collection"); G1 replaces contiguous generations with regions but keeps evacuation and aging ideas. Even the guide teaches this way: its heap-layout discussion "uses the serial collector as an example" before covering the others. And Serial is not dead weight: it "is selected by default" on non-server-class machines — fewer than two CPUs or under 1792 MB of memory — and remains the right choice for tiny single-purpose tools.

> [!warning] Promotion overload is the failure mode to name
> The young-generation contract breaks when survivors flood `To`: everything that does not fit is **promoted regardless of age**, pushing garbage-shaped churn into the old generation. The result is premature old-generation pressure, frequent Full GCs, and long compacting pauses — the classic "heap is big but everything is in Old" profile. The reverse trap also exists: assuming compaction makes old-generation allocation free — it is cheap *after* a compacting pass, which is why the pass itself is the long stop-the-world event on this collector.

> [!tip] Interview answer
> **Serial GC runs on one thread with full stop-the-world pauses. The young generation is copying collection: Eden plus two survivor spaces, one always empty; survivors are copied between them while aging, past the tenuring threshold into the old generation, and a full To-space forces early promotion. The old generation is mark-sweep-compact: mark from roots, sweep the dead, compact survivors to the start so allocation stays bump-the-pointer cheap. Parallel is literally the same design with multiple GC threads — that's the primary difference.**
