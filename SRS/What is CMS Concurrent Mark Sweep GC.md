<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/Legacy #SRS

# What is CMS Concurrent Mark Sweep GC?

> [!abstract] Short answer
> **A mostly concurrent, generational collector for the *old* (tenured) generation: short STW **initial mark** and **remark**, concurrent **trace** and **sweep**, no compaction.** Enabled with `-XX:+UseConcMarkSweepGC`. Deprecated in JDK 9, **removed in JDK 14** — that flag is ignored and you get the default collector (G1).

## What it was for

CMS targeted applications that wanted **shorter major-collection pauses** and could spare CPUs for GC threads while the mutator ran — typically a large tenured set on two or more processors. It is still **generational**: young collections are stop-the-world, in the style of the parallel collector, and can **interleave** a concurrent old-gen cycle.

A concurrent old cycle pauses the application **twice**:

1. **Initial mark** (STW, usually short) — mark objects directly reachable from roots (stacks, registers, statics, …) and from the rest of the heap (including young).
2. **Concurrent tracing (mark)** — one or more GC threads walk the live graph **while the app runs**. Throughput can drop because those CPUs are not all yours. Mutations during this phase create **floating garbage** (objects that die after they were traced); they wait for the **next** cycle. Young and old act as roots for each other.
3. **Remark** (STW, often the longer pause) — catch objects missed because references changed after CMS finished tracing them.
4. **Concurrent sweep** — reclaim unreachable objects onto **free lists** for allocation, still concurrent.

Logs also show concurrent **preclean** (work before remark) and **reset**. After the cycle, CMS idles until occupancy estimates say the tenured generation would otherwise fill. Default initiating occupancy was about **92%** of tenured (`-XX:CMSInitiatingOccupancyFraction`).

It does **not** compact/defragment old. Free space is a list of holes. If tracing/sweep cannot finish before tenured is full, or a promotion cannot find a **contiguous** block, you get **concurrent mode failure**: the app stops and the collection finishes STW (long). G1’s documented contrast: CMS cannot defragment old and eventually hits long Full GCs ([[What is G1 GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

JDK 9 deprecated it (JEP 291). JDK 14 **removed** it (JEP 363): `-XX:+UseConcMarkSweepGC` prints a warning and the VM continues with the **default** collector ([[What is the default garbage collector by Java version]], [[How does garbage collection work on the JVM]]).

```d2
direction: right
im: "Initial mark\nSTW" {
  width: 120
  height: 70
  style.fill: "#ffebee"
}
cm: "Concurrent\nmark" {
  width: 120
  height: 70
  style.fill: "#e8f5e9"
}
rm: "Remark\nSTW" {
  width: 110
  height: 70
  style.fill: "#ffebee"
}
sw: "Concurrent\nsweep" {
  width: 120
  height: 70
  style.fill: "#e8f5e9"
}
im -> cm
cm -> rm
rm -> sw
```

**Fig. 1.** Two stop-the-world pauses around concurrent mark; then concurrent sweep to free lists — not a compacting old-gen collector.

```text
# Historical (JDK 8 / 11). On JDK 14+ this is ignored.
java -XX:+UseConcMarkSweepGC YourApp
```

**Listing 1.** The only enable flag. Do not ship it on current JDKs; migrate to G1 (or ZGC) instead of tuning CMS occupancy.

> [!warning] Concurrent is not “no pauses”
> Young GCs still stop the world. Remark can rival a minor pause. Concurrent mode failure and `System.gc()` make the old generation stop-the-world. CMS also spends CPU on concurrent threads, so it is not free latency.

> [!warning] Sweep without compact fragments old
> Promotions need contiguous free chunks. Fragmentation plus a late start is how CMS earned long Full GCs. G1 evacuates/compacts regions for that reason.

> [!tip] Interview answer
> **CMS was a mostly concurrent old-gen collector: initial mark, concurrent mark, remark, concurrent sweep — it did not compact.** You enabled it with `UseConcMarkSweepGC` for shorter major pauses at the cost of CPU and fragmentation. It was deprecated in 9 and removed in 14; today you use G1 (or ZGC), not CMS flags.
