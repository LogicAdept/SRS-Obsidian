<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is garbage collector?

> [!abstract] Short answer
> A **garbage collector** is the JVM's **automatic storage management**: per the JVM Specification (§2.5.3), "Heap storage for objects is reclaimed by an automatic storage management system (**known as a garbage collector**); objects are **never explicitly deallocated**." Its job is to find objects the program can no longer use and reclaim their memory. HotSpot detects garbage by **tracing**: an object is garbage when it "can no longer be reached from any reference of any other live object" (GC Tuning Guide) — reachability starts from live threads: "A reachable object is any object that can be accessed in any potential continuing computation from any live thread" (JLS §12.6.1). The classic alternative, **reference counting**, frees an object the moment its counter hits zero but cannot reclaim **cycles**. Mechanics of the tracing walk live in [[What structures does the garbage collector analyze to find garbage]]; the collector menu lives in [[Which garbage collectors in HotSpot]].

## What the collector actually does

The GC Tuning Guide opens with the purpose: "The purpose of a garbage collector is to **free the application developer from manual dynamic memory management**." It breaks the work into four operations: allocate from memory handed over by the OS, hand that memory to the application on request, determine which parts are still in use, and reclaim the unused parts for reuse. The Spec is deliberately non-committal about *how*: the JVM "assumes no particular type of automatic storage management system, and the storage management technique may be chosen according to the implementor's system requirements" (JVMS §2.5.3). That is why different HotSpot builds ship different collectors with the same language contract — and even the *existence* of a collector is an implementation choice, not a language mandate.

## Finding garbage: tracing vs counting

Two families of approaches exist, and the difference is a favorite interview probe:

* **Reference counting** attaches a counter to every object, incremented on each new reference and decremented on each loss; zero means reclaimable. It reclaims eagerly and incrementally, but two failure modes are structural: the counters must be maintained **on every assignment** (constant overhead on the mutator), and objects that reference each other in a cycle never reach zero even when nothing outside points in — a guaranteed memory leak unless the collector adds cycle detection.
* **Tracing** flips the question: instead of asking "who points at me?", it starts from the **roots** and marks everything reachable; whatever was not marked is garbage. Cycles of unreachable objects are reclaimed **for free**, because no root path reaches them. The cost is proportional to the number of **live** objects, which is why the young-generation design matters so much — see [[How does garbage collection work on the JVM]].

```java
class Node {
    Node next;
    String label;
    Node(String label) { this.label = label; }
}

class Demo {
    public static void main(String[] args) {
        Node a = new Node("a");
        Node b = new Node("b");
        a.next = b;
        b.next = a;          // cycle: two objects referencing each other

        a = null;
        b = null;            // no live thread can reach them anymore

        // Reference counting: counters are 1 and 1 -> never reclaimed.
        // Tracing: no path from the roots -> the whole cycle is garbage.
    }
}
```

**Listing 1.** An unreachable cycle: the exact case that separates tracing collectors from naive reference counting.

```d2
direction: right
roots: "GC roots\n(live threads, statics)" {style.fill: "#e3f2fd"}
live: "reachable objects" {style.fill: "#e8f5e9"}
garbage: "unreachable cycle\na <-> b" {style.fill: "#ffebee"}
reclaim: "reclaimed" {style.fill: "#f0f0f0"}
roots -> live: "trace"
garbage -> reclaim: "no root path"
```

**Fig. 1.** Tracing defines garbage negatively: everything without a root path is reclaimable, cycles included.

## What a collector does not promise

Automatic memory management removes *deallocation* from the programmer's checklist, not *lifecycle design*. A long-lived static collection that quietly accumulates entries keeps them reachable — reachability, not intent, is what the collector obeys, which is why leak diagnosis starts from a heap dump. There is also no tie to *when* reclamation happens: the collector works "by its own discretion," and `System.gc()` only "suggests that the Java Virtual Machine expend effort toward recycling unused objects" (Javadoc). Resource cleanup therefore belongs to explicit constructs — try-with-resources, `close()` — not to the collector. How to investigate retention problems is in [[How do you diagnose memory pressure and OutOfMemoryError]].

> [!warning] "Reference counting" is not how HotSpot works
> Answering "the JVM counts references and frees at zero" is a rejection-level mistake in interviews: it is falsified by the cycle case, which Java demonstrably handles — a cyclic structure left unreachable **is** reclaimed. Reference counting exists in the wild (CPython uses it plus a separate cycle detector), but HotSpot is a tracing collector from GC roots. The second trap is the mirror image: assuming a *tracing* collector cannot leak. It cannot leak by miscounting, but reachable-forever objects (statics, caches without eviction) are retained just the same.

> [!tip] Interview answer
> **A garbage collector is the JVM's automatic memory manager: the JVM Spec says heap storage is reclaimed by an automatic storage management system known as a garbage collector, and objects are never explicitly deallocated. Garbage is defined by reachability — anything a live thread can still access stays; HotSpot finds it by tracing from GC roots, so unreachable cycles are reclaimed too, unlike naive reference counting which leaks cycles. The collector decides when to run; it's not a resource-cleanup mechanism — that's what try-with-resources is for.**
