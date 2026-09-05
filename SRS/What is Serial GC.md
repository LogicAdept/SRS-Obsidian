<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is Serial GC?

> [!abstract] Short answer
> **The single-threaded, stop-the-world, generational collector.** One GC thread does all collection work. Enable with `-XX:+UseSerialGC`. It fits **single-processor** machines and **small heaps** (about 100 MB), and is still the ergonomic default on some constrained configurations. It is not “the collector for single-threaded apps.”

## One thread, same generations

Serial is the simple HotSpot collector: **one thread**, no coordination between GC workers, so little communication overhead. It **cannot** use extra CPUs for collection. On multiprocessors it is still reasonable for **small data sets** (guide figure: up to about **100 MB**). The Java 21 selection guide also picks it when the app runs on **one processor** and there are no pause-time requirements ([[How does garbage collection work on the JVM]], [[What is the default garbage collector by Java version]]).

It is **generational**, and the tuning guide’s heap pictures (eden, two survivor spaces, old, copy-on-minor, promote by aging or overflow) are drawn for Serial. A **minor** collection stops the world and copies live young objects with that one thread. A **major** collection stops the world over the heap on the same thread. Parallel is this design with **many** GC threads and compacting old as a whole; G1 is regional and mostly concurrent ([[What is Parallel GC]], [[What is G1 GC]], [[What are garbage collector generations]], [[How would you explain major garbage collector algorithms on the JVM]]).

The Java 21 man page: best for **small and simple** applications that need no special GC behavior. `-XX:+UseSerialGC` is off by default in the sense that you get the **ergonomic** collector (usually G1); Serial is still chosen automatically on **certain hardware and OS** setups. On a large multiprocessor server, G1 is the usual default — do not ship Serial there hoping for “simpler pauses.”

```d2
direction: down
stw: "Stop the world" {
  width: 220
  height: 45
  style.fill: "#ffebee"
}
one: "One GC thread\nyoung copy + old collect" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
fit: "1 CPU or ~100 MB live" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
stw -> one
one -> fit
```

**Fig. 1.** Serial is fully stop-the-world. Extra cores sit idle during GC. That is a feature on a tiny heap and a bug on a 16-core service.

```text
java -XX:+UseSerialGC -Xmx128m YourApp
```

**Listing 1.** Explicit Serial plus a small heap. On Java 21, omitting the flag usually means G1 unless ergonomics pick Serial for you.

> [!warning] Single *processor*, not single *application thread*
> A multi-threaded app on one CPU can still use Serial. A single-threaded app on many CPUs still pays a long STW pause on that one GC thread. The dump slogan swaps those.

> [!warning] Do not teach “mark-sweep-compact” as Serial’s official old-gen name
> Young copying is documented for the serial layout. The Java 21 guide does not brand Serial old as Mark-Sweep-Compact. Recite one thread, STW, generational copy/promote — not a textbook MSC pipeline.

> [!tip] Interview answer
> **Serial GC is one thread, stop-the-world, generational — the simple collector for small heaps and single-CPU boxes.** Enable it with `UseSerialGC`. Parallel is the same idea with many GC threads; G1 is the usual default on servers. It is not the right default for a large multi-core service.
