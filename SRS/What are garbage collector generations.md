<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What are garbage collector generations?

> [!abstract] Short answer
> **Age-based heap pools so HotSpot can collect *young* objects often and *old* ones rarely.** Most allocations land in **eden**. Survivors are **copied** between two survivor spaces until they are **aged** into the **old** generation. A **minor** collection touches only young; a **major** collection typically takes the whole heap.

## Why split the heap by age

A naive collector traces every live object every time. Generational collection uses the **weak generational hypothesis**: most objects die young. HotSpot therefore manages the heap as **generations** — pools of different ages — and runs a collection when that pool fills ([[How does garbage collection work on the JVM]], [[How would you explain major garbage collector algorithms on the JVM]]).

**Young generation** (Serial/Parallel layout):

- **Eden** — almost all new objects are allocated here.
- **Two survivor spaces** — one is empty and is the **to**-space. A **minor** collection copies live objects from eden and the other survivor space into that empty space; then eden and the source survivor are empty. Next time the two survivors swap roles.
- Objects bounce between survivors until they have been copied **enough times** (aging / tenuring) or **there isn’t room**. Then they are copied into **old**. That overflow path is why “survived N minor GCs” is incomplete.

Cost of a minor collection tracks **live objects copied**, so a nursery full of garbage is cheap.

**Old generation** — objects that were promoted. When it fills, a **major** collection usually scans the **entire heap** and lasts longer. Parallel compactes old **as a whole**. G1 still has young vs old, but as **regions** (eden, survivor, old, humongous) laid out noncontiguously; mixed collections evacuate some old regions without always doing a full heap ([[What is G1 GC]], [[What are Minor GC and Full GC]]).

G1 is generational by default. ZGC in Java 21 is generational only with `-XX:+ZGenerational`. **Metaspace** is class metadata in native memory, not a third heap generation (PermGen is gone) ([[What JVM runtime memory regions exist]]).

```d2
direction: right
eden: "Eden\n(new objects)" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
from: "Survivor\n(from)" {
  width: 140
  height: 70
  style.fill: "#fff8e1"
}
to: "Survivor\n(to, empty)" {
  width: 150
  height: 70
  style.fill: "#fff8e1"
}
old: "Old\n(promoted)" {
  width: 140
  height: 70
  style.fill: "#e3f2fd"
}
eden -> to: "minor: copy live"
from -> to: "minor: copy live"
to -> old: "aged or overflow"
```

**Fig. 1.** Serial-style young generation: copy into the empty survivor, promote when aged or when survivors overflow. G1 uses the same idea on regions, not one contiguous S0/S1 pair.

```text
# Observe aging (tenuring threshold) in logs — not a generation size knob
java -Xlog:gc,age YourApp
```

**Listing 1.** HotSpot can log the copy-count threshold that keeps survivors about half full. Pinning young size with `-Xmn` is a Parallel-era habit; on G1 it fights pause-time control.

> [!warning] Promotion is not “after a few minor GCs” only
> The spec-level HotSpot story is **copy count** or **not enough survivor space**. A burst of live data can tenure in one minor collection.

> [!warning] S0/S1 is a diagram, not G1’s layout
> Interview pictures label two survivor chunks From/To. G1’s young generation is a **set of regions** that need not sit next to each other. Humongous allocations go to old-style regions, not eden.

> [!tip] Interview answer
> **Generations are heap pools by object age so we collect the nursery cheaply.** New objects go to eden, live ones are copied through two survivors, then promoted to old. Minor GC is young only; major GC is the expensive whole-heap (or G1 mixed/full) work. G1 regions are the same idea; Metaspace is not a generation.
