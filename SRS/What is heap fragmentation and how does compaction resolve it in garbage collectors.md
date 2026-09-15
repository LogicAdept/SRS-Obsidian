<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/JVM/Memory #SRS

# What is heap fragmentation and how does compaction resolve it in garbage collectors?

> [!abstract] Short answer
> **Fragmentation is free heap memory split into small non-adjacent holes, so an allocation can fail although the total free space suffices; compaction slides live objects together to rebuild contiguous blocks.** The tuning guide lists compaction as a core HotSpot technique: "try to recover larger contiguous free memory by compacting live objects." Region-based collectors get the same effect by evacuating live objects out of chosen regions.

## The problem: enough bytes, no contiguous block

A collector that only **sweeps** — reclaims dead objects in place — leaves their space behind live survivors as scattered holes. The heap then has enough total free memory for a new object but no single run of it, and allocation fails anyway. The guide names the remedy among the techniques HotSpot collectors employ: "try to recover larger contiguous free memory by compacting live objects" — moving survivors toward one end of the space so the free area becomes one block again. Contiguity is not cosmetic: allocation into a compacted region is a cheap pointer bump, while allocating from a fragmented free list must search for a fitting hole. JVMS 2.5.3, notably, only says "the memory for the heap does not need to be contiguous" — contiguity is a HotSpot performance choice, not a spec requirement ([[How does the Serial GC work]]).

## Where fragmentation comes from in HotSpot

| Source | Official description |
| --- | --- |
| **Promotion races** | "Some fragmentation is possible due to promotions from the young generation to the old generation during the collection" — multiple GC threads promote survivors into old concurrently (guide, Parallel chapter) |
| **G1's expected workload** | G1 suits heaps with "a significant amount of fragmentation in the heap" — it is built to absorb it |
| **Humongous objects** | "Humongous Object Fragmentation": "a Full GC could occur before all Java heap memory has been exhausted due to the necessity of finding a contiguous set of regions" for humongous allocations; remedy is `-XX:G1HeapRegionSize` or a bigger heap |

The Parallel collector compacts the old generation to fight exactly this; G1 makes fragmentation manageable at region granularity — evacuation empties the worst regions and reuses them whole ([[What is G1 GC]], [[What are garbage collector generations]]).

## How each collector reaches contiguity

Serial and Parallel **slide-compact** the old generation: mark live from the roots, sweep the dead, then move survivors to the start of the space — one long stop-the-world pass, which is why their Full GCs are the pauses to fear. Region-based collectors — G1, ZGC, Shenandoah — reach the same state by **evacuation**: live objects are copied into fresh regions, and the emptied source regions become contiguous free space by construction; ZGC and Shenandoah even do that copying concurrently. CMS is the cautionary case: it swept the old generation without compacting, accepting hole-riddled old space and the eventual full-compaction bill — the trade that led to its deprecation (JEP 291) after G1 absorbed its role ([[What is CMS Concurrent Mark Sweep GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

```java
// Humongous allocations are where fragmentation bites G1 first:
//   java -XX:+UseG1GC -Xlog:gc -Xmx64m -XX:G1HeapRegionSize=1m FragDemo
//
//   GC(2) Pause Young (Normal) ... Humongous regions: 12->0
class FragDemo {
    public static void main(String[] args) {
        for (int i = 0; i < 30; i++) {
            // half a megabyte: spans multiple 1m regions -> humongous
            byte[] big = new byte[512 * 1024];
            java.util.Objects.requireNonNull(big);
        }
        System.out.println("long-lived humongous objects pin contiguous regions");
    }
}
```

**Listing 1.** Objects larger than half a region size are humongous and need contiguous region runs; churn that is collected promptly shows up shrinking in the `Humongous regions` counter, while long-lived humongous objects are the fragmentation pattern behind G1 Full GCs.

```d2
direction: down
frag: "Fragmented space\nL H H L H L H" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}
fail: "Allocate 3 slots:\nno contiguous hole -> fail" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
compact: "Compact live objects\nL L L H H H H H" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
ok: "Allocate 3 slots:\ncontiguous block -> done" {
  width: 290
  height: 55
  style.fill: "#e3f2fd"
}
frag -> fail
frag -> compact -> ok
```

**Fig. 1.** Sweeping leaves holes between live objects (L) and reclamation fails on request size; compaction slides survivors together and hands allocation one contiguous block.

> [!warning] "Fragmentation only matters in the old generation" — half right
> The young generation avoids fragmentation structurally: its survivors are copied into fresh survivor space every collection, which compacts by construction. But young promotion into a fragmented old generation is exactly where the guide locates Parallel's fragmentation risk, and humongous allocations skip the young generation entirely — the problem leaks into every generation choice.

> [!warning] Compaction is not free
> Sliding compaction moves every live object and therefore costs a full stop-the-world pass on Serial and Parallel; region-based collectors pay in copying work and reserve headroom for evacuation. The contiguous-heap end state is cheap to allocate from — the pass that builds it is the expensive part ([[What is a stop the world pause in garbage collection and why do collectors minimize it]]).

> [!tip] Interview answer
> **Fragmentation is free memory broken into non-adjacent holes, which makes allocations fail despite enough total space; compaction repairs it by moving live objects together.** Serial and Parallel compact the old generation in a full STW pass; G1, ZGC, and Shenandoah evacuate live objects into fresh regions, which compacts by construction; CMS swept without compacting and paid for it. Watch humongous objects — they need contiguous region runs and are G1's classic fragmentation trigger.

Related: [[What is G1 GC]], [[What is Parallel GC]], [[What is Serial GC]], [[What are Minor GC and Full GC]], [[What is the heap problem pattern]]
