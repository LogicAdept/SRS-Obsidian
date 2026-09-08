<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How would you explain the Java garbage collector?

> [!abstract] Short answer
> **Java does not `free` objects.** The VM traces from GC roots, treats unreachable objects as garbage, and reclaims their heap storage. HotSpot is generational (copy in young, promote survivors) and, on Java 21, usually runs **G1**. You size the heap and pick a collector at launch; `System.gc()` is only a hint.

## Automatic storage, then HotSpot’s shape

Start with the language: storage for class instances and arrays is on the **heap**, reclaimed by an automatic collector. There is no `delete`. An object is garbage when it is **unreachable** — a live thread could not use it in a continuing computation. Incoming pointers among dead objects do not keep them; the collector **traces** from roots (live threads, reachable statics, JNI, VM internals), not by counting fields ([[How does the garbage collector decide an object can be collected]], [[How does garbage collection treat cyclic references between live objects]]).

Walking every live object on every cycle would scale with the live set. HotSpot therefore bets on the **weak generational hypothesis**: most objects die young. New objects go in **eden**. A **minor** collection copies survivors through **survivor** spaces and **promotes** the rest into **old**. A **major** collection of old (or G1 mixed/full work) is rarer and more expensive. That is *how* the collector uses the heap, not extra spec areas besides heap vs stacks vs method area ([[What JVM runtime memory regions exist]], [[What are garbage collector generations]]).

Collectors are algorithms on that tracing + (usually) generational skeleton ([[How would you explain major garbage collector algorithms on the JVM]], [[How does garbage collection work on the JVM]]):

- **G1** — usual Java 21 default. Heap as equal **regions**; evacuates garbage-first; concurrent marking; pause-time *goal*.
- **Parallel** — many GC threads, throughput; compact old as a whole. Server default before JDK 9.
- **Serial** — one GC thread; small heaps / single CPU.
- **ZGC** — concurrent relocate, sub-millisecond pauses, huge heaps; in 21 generational mode is `-XX:+ZGenerational`.
- **CMS** — concurrent mark-sweep; removed in JDK 14.

You do **not** drive this from application code. `System.gc()` suggests a collection and can be ignored (`-XX:+DisableExplicitGC`). Real knobs are `-Xms`/`-Xmx`, the collector flag, and Metaspace limits ([[Can developers control garbage collection or JVM memory settings]]).

```d2
direction: down
lang: "No free — heap instances/arrays" {
  width: 280
  height: 50
}
trace: "Trace from roots\nunreachable = garbage" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
gen: "Young copy / promote\nold less often" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
pick: "G1 default; or Parallel / Serial / ZGC" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
lang -> trace
trace -> gen
gen -> pick
```

**Fig. 1.** Explain in this order: automatic heap, reachability, generations, then which collector.

```java
public final class GcExplain {
    public static void main(String[] args) {
        Object live = new Object(); // reachable from a stack local
        Object garbage = new Object();
        garbage = live;             // previous instance has no root path
        System.out.println(live);
        // garbage's first instance is eligible; collection is the VM's timing
    }
}
```

**Listing 1.** Dropping the last root makes an instance garbage. Printing `live` does not collect anything; the next young/old cycle does.

> [!warning] Do not explain GC as “no references left”
> A cycle with no path from a thread is already garbage. A `static` cache is a root. Soft/weak/phantom refs are a weaker ladder, not extra strong roots ([[What reference types exist in Java such as strong weak soft and phantom]]).

> [!warning] G1’s pause flag is a goal
> `-XX:MaxGCPauseMillis` is not a real-time SLA. Full GC can still be long. Concurrent collectors still pause, just less.

> [!tip] Interview answer
> **The Java GC automatically reclaims heap objects that are unreachable from roots — we never free them.** HotSpot traces, copies in the young generation, and promotes survivors. On current JDKs you usually get G1; pick Parallel for throughput or ZGC for tiny pauses, and tune the heap rather than calling `System.gc()`.
