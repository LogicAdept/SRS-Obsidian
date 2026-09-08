<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/JVM/Memory #SRS

# What structures does the garbage collector analyze to find garbage?

> [!abstract] Short answer
> HotSpot collectors are **tracing**: they do not hunt “unused” objects. They walk **paths from GC roots** and treat anything **without** such a path as unreachable, hence eligible to collect. Roots include **live-thread** state (stacks and registers) and **internal JVM** references (for example statics). A **young / incremental** pause also treats **remembered-set** locations and **compiled-code** oops as roots **into the collection set** — [[How would you explain the JVM stack and stack frames]], [[What are garbage collector generations]].

## Trace live objects; the rest is garbage

JLS: an object is **reachable** if some **live thread** can still access it in a potential continuing computation. The HotSpot GC Tuning Guide: it is **unreachable** (eligible) when there is **no path from a GC root**. Roots are **references from an active thread** and **internal JVM references** — the pointers that keep objects in memory. CMS’s initial-mark pause names the usual examples: **thread stacks**, **registers**, **static objects**, plus **other heap** areas (young generation as roots into old).

Then the collector **follows fields** of those objects (the object graph). Cycles among objects that no root can reach still die; Java GC is **not** reference counting — [[What reference types exist in Java such as strong weak soft and phantom]]. Soft/weak/phantom wrappers change **which** paths count as strong reachability; they are not extra heap spaces.

**Generational / G1 incremental work.** A pause often collects only a **collection set**. G1’s evacuate phase starts from three kinds of **root into that set**:

| Kind | Structure scanned |
| --- | --- |
| **External roots** | VM-internal pointers outside the collection set (thread stacks and registers, statics, …) — G1 log: `Ext Root Scanning` |
| **Code roots** | Embedded oops in **JIT code** — `Code Root Scan` |
| **Heap roots** | Locations **outside** the collection set that may point **in**, found via **remembered sets** of **cards** (default 512-byte heap tiles) — `Scan Heap Roots` |

A remembered set is **not** the object graph. It is an index of **where to look** for cross-region pointers so a young collection need not scan the entire old generation.

```java
public final class GcRootsDemo {
    static Object keptByClass; // static — a typical internal root

    public static void main(String[] args) {
        byte[] keptByFrame = new byte[32];
        byte[] unreachable = new byte[32];
        unreachable = null;
        keptByClass = keptByFrame;
        System.out.println(keptByFrame.length);
    }
}
```

**Listing 1.** After `unreachable = null` there is no path from a live thread to that array. `keptByFrame` lives in the current **frame**; `keptByClass` is a **static**. Those are the structures a tracer starts from — not a full-heap “unused object” scan.

```d2
direction: down
roots: "GC roots\nthreads (stacks, registers)\nVM internals, code oops" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
rs: "Remembered sets / cards\n(heap roots into the CSet)" {
  width: 320
  height: 55
  style.fill: "#fff8e1"
}
live: "Reachable object graph" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
dead: "No path from a root → garbage" {
  width: 280
  height: 45
  style.fill: "#fce4ec"
}
roots -> live
rs -> live
live -> dead: "unmarked"
```

**Fig. 1.** Analyze **roots** and then **outgoing references**. Remembered sets only tell a **partial** collection where old-to-young (or other cross-region) pointers sit.

> [!warning] The collector does not “scan the heap for garbage”
> It **marks / copies live** objects from roots. Unreachable memory is reclaimed as a **side effect**. Interview answers that start with “it looks at every object’s age” skip the root set. Age and generations decide **when** a region is collected, not **what counts as live** — [[What JVM runtime memory regions exist]].

> [!warning] JVMS does not pick an algorithm
> The spec only says the heap is reclaimed by an automatic manager and that frames hold **references**. Root lists, card tables, and remembered sets are **HotSpot**. A young collection that ignored remembered sets would miss old-to-young pointers and collect live objects.

> [!tip] Interview answer
> Garbage is whatever has no path from a GC root. HotSpot traces live-thread stacks and registers plus internal JVM pointers such as statics, then follows object fields. For a young or G1 incremental pause it also scans remembered-set cards and oops in compiled code as roots into the collection set.
