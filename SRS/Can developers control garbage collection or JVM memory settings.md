<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/JVM/Tuning #SRS

# Can developers control garbage collection or JVM memory settings?

> [!abstract] Short answer
> **Yes — extensively, but through policy, not commands.** The JVM Spec explicitly allows it: "A Java Virtual Machine implementation may provide the programmer or the user control over the **initial size** of the heap, as well as ... control over the **maximum and minimum heap size**" (JVMS §2.5.3). On the command line (Java 21): **`-Xms`/`-Xmx`** set initial/maximum heap, **`-Xmn`** and **`-XX:NewRatio`**/`-XX:SurvivorRatio`` shape the generations, **`-XX:MaxTenuringThreshold`** sets the promotion age, **`-XX:+UseSerialGC`/`UseParallelGC`/`UseG1GC`/`UseZGC`** pick the collector, **`-Xlog:gc`** exposes every pause. Without flags, **ergonomics** decide: "Garbage-First (G1) Collector on server-class machines, Serial Collector otherwise", initial heap **1/64** and maximum **1/4** of physical memory. What you **cannot** do is dictate *when* collection happens — `System.gc()` merely "suggests" and can be disabled with `-XX:+DisableExplicitGC`. The step-by-step knobs live in [[How would you explain tuning garbage collector settings on the JVM]]; the collectors being switched: [[Which garbage collectors in HotSpot]].

## What is controllable, layer by layer

The Tuning Guide's position: ergonomics pick good defaults — "Use these defaults before using the more detailed controls described in subsequent sections" — and explicit control is for when measurements say otherwise. The practical layers:

* **Heap sizing.** `-Xms` (initial) and `-Xmx` (maximum) bound the heap; the Spec leaves room for exactly this by saying the heap "may be of a fixed size or may be expanded as required by the computation and may be contracted". Ergonomic defaults: 1/64 and 1/4 of physical memory respectively.
* **Generation shape.** `-Xmn` sizes the young generation; `-XX:NewRatio` and `-XX:SurvivorRatio` set old-to-young and eden-to-survivor proportions; `-XX:MaxTenuringThreshold` influences how many survivor copies precede promotion. These translate directly into how often minor collections run — see [[What are Minor GC and Full GC]].
* **Collector choice and goals.** The four `-XX:+Use...GC` switches, plus goal knobs: "Maximum Pause-Time Goal" and "Throughput Goal" — "behavior-based tuning dynamically optimizes the sizes of the heap to meet a specified behavior".
* **Observability.** `-Xlog:gc` (Unified Logging) prints each collection with before/after heap and pause duration — the feedback loop every other knob depends on.

```java
// A realistic production layout (Java 21), one flag per decision:
//   java -Xms2g -Xmx2g \                # fixed-size heap: no resize pauses
//        -XX:+UseG1GC \                 # collector by requirement
//        -XX:MaxTenuringThreshold=8 \   # let slower survivors age longer
//        -XX:+DisableExplicitGC \       # reject System.gc() calls from libraries
//        -Xlog:gc,gc+heap=info:file=gc.log:time,uptime:filecount=5,filesize=20m
class Bootstrap {
    public static void main(String[] args) {
        System.out.println("JVM up: inspect gc.log and jcmd <pid> GC.heap_info");
    }
}
```

**Listing 1.** Control is exercised entirely at process start: sizing, collector, promotion policy, explicit-GC policy, and logging are all command-line decisions.

```d2
direction: right
start: "Start JVM" {style.fill: "#e3f2fd"}
flags: "flags given?\n-Xms -Xmx UseG1GC ..." {style.fill: "#fff3e0"}
ergo: "ergonomics:\nserver-class -> G1\nelse Serial; heap 1/64..1/4 RAM" {style.fill: "#fff8e1"}
run: "run with chosen policy" {style.fill: "#e8f5e9"}
observe: "-Xlog:gc + goals\n(pause time, throughput)" {style.fill: "#e8f5e9"}
retune: "resize / re-select\nbased on measurements" {style.fill: "#ffebee"}
start -> flags
flags -> ergo: "no"
flags -> run: "yes"
ergo -> run
run -> observe -> retune -> flags
```

**Fig. 1.** Two paths to a configuration — explicit flags or ergonomics — closed by a measurement loop; defaults are the intended starting point.

## What is deliberately not controllable

The Spec hands over *sizing and selection*, not *scheduling or targeting*. No flag says "collect now", and none says "free this object": reclamation still follows reachability, so tuning cannot mask a leak — it can only delay the `OutOfMemoryError`. `System.gc()` is the strongest push available and the Javadoc keeps it a suggestion: "Calling the gc method suggests that the Java Virtual Machine expend effort toward recycling unused objects ... the Java Virtual Machine has made a best effort" — and production code routinely **forbids** it via `-XX:+DisableExplicitGC`, because whole-heap collections triggered by third-party libraries are a latency hazard. Even goal-based tuning is honest about limits: the guide notes goals "can't always be met" — an application needs a minimum heap just to hold its live data.

> [!warning] Tuning is not a leak fix, and `-Xmx` is not free
> Two recurring interview myths. First: "set `-Xmx` big enough and GC problems disappear" — a bigger heap only lengthens the cycle; a leak fills *any* heap, and with classic collectors a full one means longer, worse compacting pauses. Second: "call `System.gc()` before a latency-sensitive window to clean up" — it is a suggestion that libraries can trigger, it cannot reclaim unreachable-but-referenced objects, and disabling it is standard practice. Control exists over *shape and schedule*, never over *individual objects*; the honest escalation path is measure (heap dump, `gc` log), then retune, then fix the code.

> [!tip] Interview answer
> **Yes, developers control GC and memory through JVM flags, not through code commands. You size the heap with -Xms and -Xmx, shape generations with -Xmn, NewRatio, SurvivorRatio and MaxTenuringThreshold, pick the collector with the Use-GC switches, and watch everything through -Xlog:gc. Without flags, ergonomics apply: G1 on server-class machines, Serial otherwise, heap between 1/64 and 1/4 of physical memory. What you can't do is command a collection — System.gc only suggests and is usually disabled — or reclaim any specific object; reachability decides that, so tuning shapes policy while leaks are fixed in code.**
