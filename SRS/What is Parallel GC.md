<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is Parallel GC?

> [!abstract] Short answer
> **The throughput collector: same generational copy/promote story as Serial, but *many* GC threads for both minor and major collections.** Enable with `-XX:+UseParallelGC`. Pick it when peak throughput matters and pauses of about a second (or more) are acceptable. It is stop-the-world, not concurrent. It was the server default before JDK 9; G1 is the usual default now.

## Throughput, not tiny pauses

Parallel GC is a **generational** collector like Serial. The difference is **multiple threads** to finish collections faster on multiprocessor hardware, for medium-to-large data sets. With `-XX:+UseParallelGC`, **both young and old** collections run in parallel. Old is still compacted **as a whole** in one pause — unlike G1’s mixed regional evacuate ([[What is G1 GC]], [[What is Serial GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

The Java 21 selection guide: use Parallel when (a) peak application performance is first and (b) there is no pause-time requirement, or pauses of **one second or longer** are fine. For shorter pauses, G1 or ZGC. On **one** processor, Parallel is often *worse* than Serial because of synchronization overhead; it pulls ahead around two CPUs and more.

Goals, in order: optional **max pause** hint (`-XX:MaxGCPauseMillis`, *no* default pause goal — unlike G1’s 200 ms), then **throughput** (`-XX:GCTimeRatio`, default **99** → about **1%** of time in GC pauses), then smaller footprint. Missing the throughput goal often means grow the heap. Thread count is `-XX:ParallelGCThreads` (ergonomic from available CPUs). Adaptive generation sizing is on by default (`UseAdaptiveSizePolicy`).

It is still **stop-the-world** for those collections: more workers shorten the pause, they do not collect beside the mutator. Parallel minor collections can **fragment** old: each worker keeps a promotion buffer. Fewer GC threads or a larger old generation reduces that. UseGCOverheadLimit still applies (about 98% time in GC and under 2% recovered → `OutOfMemoryError`) ([[How does garbage collection work on the JVM]], [[What are garbage collector generations]]).

JDK 9 made **G1** the default on server configurations (JEP 248); Parallel had been that default. On Java 21, `-XX:+UseParallelGC` is off unless you set it; the man page’s default collector is G1 ([[What is the default garbage collector by Java version]]).

```d2
direction: down
serial: "Serial: one GC thread\nSTW young + old" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
par: "Parallel: many GC threads\nSTW young + old compact" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
goal: "Maximize application time\n(GCTimeRatio), not min pause" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
serial -> par: "same generations"
par -> goal
```

**Fig. 1.** Parallel is Serial’s algorithm with a thread pool on the pause, aimed at throughput. It is not CMS/G1-style concurrent marking.

```text
java -XX:+UseParallelGC -XX:GCTimeRatio=99 -Xms4g -Xmx4g YourApp
```

**Listing 1.** Throughput collector, default ~1% GC-time goal, heap sized for fewer pauses. Add `MaxGCPauseMillis` only as a hint — it may sacrifice throughput and still miss the number.

> [!warning] “Parallel” is not “concurrent”
> Application threads stop for minor and major work. Extra GC threads make that pause shorter on many CPUs. They do not run a CMS/G1 concurrent mark beside the mutator.

> [!warning] Not “the Java 8 default” on every machine
> It was the **server** default until G1 in JDK 9. Client/small configs used Serial then, and some still do. Reciting “default until 8 inclusive, G1 from 9 on everything” is too sharp.

> [!tip] Interview answer
> **Parallel GC is the throughput collector: many threads, stop-the-world, generational, compacting old as a whole.** Use `UseParallelGC` when you care about batch work and can live with longer pauses. G1 is the usual default since 9 on servers. It is not a low-pause concurrent collector.
