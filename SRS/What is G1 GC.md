<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is G1 GC?

> [!abstract] Short answer
> **Garbage-First: the usual HotSpot default collector.** It splits the heap into equal **regions** (eden, survivor, old, humongous), **evacuates** (copies) live objects from the most garbage-filled regions first, and aims at a pause-time **goal** (`-XX:MaxGCPauseMillis`, default 200 ms) — not a real-time SLA. Enable with `-XX:+UseG1GC`.

## Regions, then a two-phase cycle

G1 is generational, incremental, parallel, **mostly concurrent**, stop-the-world, and **evacuating**. It is aimed at multiprocessor machines with a lot of RAM: heaps up to tens of GB (or larger), often more than half live, allocation rates that swing, some fragmentation, and pause targets of a **few hundred milliseconds**. It trades some throughput (concurrent GC threads) for shorter, more uniform pauses than compacting all of old in one go ([[How would you explain major garbage collector algorithms on the JVM]], [[What is Parallel GC]]).

The heap is a grid of equal **regions**. Each region is empty or young (eden / survivor) or old. Objects that span multiple regions are **humongous** and are treated as old. Application allocation is into eden, except humongous objects. Regions need not be contiguous, unlike Serial’s one eden + two survivor chunks ([[What are garbage collector generations]]).

Space is reclaimed by **evacuation**: copy live objects out of a **collection set** into other regions (which **compacts** them). Young objects go to survivor or old by age; old objects go to other old regions. G1 prefers regions that are mostly garbage — that is the “garbage-first” name.

Cycle (Java 21):

1. **Young-only** — normal young collections that promote into old.
2. When old occupancy hits the initiating threshold, a **Concurrent Start** young collection begins **concurrent marking** of live objects in old (not a separate collector named “Copy”).
3. **Remark** and **Cleanup** (STW) finish marking, references, class unloading, and decide whether mixed work is worth it.
4. **Space-reclamation / mixed** — young plus selected old regions in the same pauses, until further old regions would not pay. Then young-only starts again.
5. Backup: **Full GC** — in-place stop-the-world compact of the whole heap if memory runs out while marking.

`-XX:MaxGCPauseMillis` is a **soft** goal. G1 sizes young generation to try to meet it; pinning `-Xmn` fights that ([[How would you explain tuning garbage collector settings on the JVM]]). It replaced CMS as the intended low-pause server collector; CMS is gone ([[What is CMS Concurrent Mark Sweep GC]]). G1 became the default on server configurations in JDK 9 (JEP 248) and is the usual default on Java 21; some small/single-CPU setups still ergonomically pick Serial ([[What is the default garbage collector by Java version]], [[How does garbage collection work on the JVM]]).

```d2
direction: down
y: "Young-only\n(evacuate eden/survivors)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
cs: "Concurrent Start + mark\n(old liveness)" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
mix: "Mixed: young + garbage-first old" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
y -> cs: "old occupancy / IHOP"
cs -> mix: "Remark + Cleanup"
mix -> y: "not enough old gain"
```

**Fig. 1.** Evacuate young continuously; mark old concurrently; then mix in the emptiest old regions. Copying is how every pause reclaims space, not a fifth named phase after Cleanup.

```text
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xmx4g YourApp
```

**Listing 1.** G1 is already the usual default; the flag makes it explicit. `MaxGCPauseMillis` is a goal, not a cap. Full GC in logs still means the live set or humongous objects beat the plan.

> [!warning] G1 is not real-time
> It tries to hit the pause target with high probability over time, not for every pause. Evacuation failure and Full GC (in-place compact) can be very slow.

> [!warning] Do not recite CMS’s five phase names as G1
> Dump lists Initial Mark / Concurrent Mark / Remark / Cleanup / Copy. Java 21’s story is young-only, **Concurrent Start**, concurrent mark, Remark, Cleanup, **mixed** evacuation. Copying happens inside those STW pauses.

> [!tip] Interview answer
> **G1 is the default region-based collector: it copies live objects out of the garbage-first regions and aims at a pause-time goal.** Concurrent marking of old, then mixed collections, instead of compacting all of old like Parallel or sweeping holes like CMS. Enable with `UseG1GC`; do not treat `MaxGCPauseMillis` as a hard SLA.
