<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is ZGC?

> [!abstract] Short answer
> **HotSpot’s scalable low-latency collector: expensive work runs concurrently, pauses are meant to stay around a millisecond and not grow with heap size.** Enable it with `-XX:+UseZGC`. It is suitable for latency-sensitive apps on heaps from a few hundred MB to 16 TB. It is **not** the default collector (that stays G1). In Java 21, young/old splitting is opt-in: `-XX:+ZGenerational`.

## Concurrent relocate with colored pointers

JEP 333 (experimental in **JDK 11**, Linux/x64): ZGC is a concurrent, region-based, NUMA-aware, **compacting** collector. Stop-the-world work is limited to **root scanning**, so pause length is not supposed to track heap size or live-set size. The mechanism is **colored pointers** plus **load barriers**: a Java thread that loads a reference from the heap hits a barrier; the extra bits on the pointer tell the barrier whether the object already moved, so relocation can run while mutators run. That is a different trick from Shenandoah’s per-object forwarding pointer ([[What is Shenandoah GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

The original JEP **goal** was pauses not exceeding **10 ms** (not a hard SLA). The Oracle ZGC chapter documents the product collector as doing the expensive work concurrently **without stopping application threads for more than a millisecond**, independent of heap size.

JEP 377 (**JDK 15**): product feature. `-XX:+UnlockExperimentalVMOptions` is no longer required with `-XX:+UseZGC`. It does **not** become the default (G1 stays). Max heap went to **16 TB** (from 4 TB); unused memory can be uncommitted (JEP 351).

JEP 439 (**JDK 21**): **generational** ZGC. Plain `-XX:+UseZGC` is still the older single-generation collector that re-scans the whole live set. `-XX:+UseZGC -XX:+ZGenerational` collects young and old independently (store barriers as well as load barriers). JEP 474 (**JDK 23**) makes generational the default for ZGC and deprecates non-generational. JEP 490 (**JDK 24**) **removes** non-generational mode: `UseZGC` is generational; `ZGenerational` is obsolete.

Because relocation is concurrent, `-Xmx` must cover the live set **plus headroom** so allocation can continue during a cycle. The main tuning knob is maximum heap size; `-XX:SoftMaxHeapSize` is a soft cap ZGC tries to stay under. ZGC is in the Oracle Java 21 catalog next to Serial, Parallel, and G1 ([[What is G1 GC]], [[What is the default garbage collector by Java version]]).

```d2
direction: down
g1: "G1: concurrent mark\nSTW evacuate regions" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
z: "ZGC: concurrent mark\nand concurrent relocate" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
mech: "Colored pointers +\nload barrier on heap loads" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
pause: "STW ≈ root scan\n~1 ms, not heap size" {
  width: 260
  height: 55
  style.fill: "#f3e5f5"
}
g1 -> z: "same low-pause goal,\ndifferent compact"
z -> mech
mech -> pause
```

**Fig. 1.** ZGC keeps mutators running while it moves objects. G1 still stops the world to evacuate. Neither is a real-time collector.

```text
# Java 21: generational mode is opt-in
java -XX:+UseZGC -XX:+ZGenerational YourApp

# JDK 15–20, or 21 without +ZGenerational: non-generational ZGC
java -XX:+UseZGC YourApp
```

**Listing 1.** Enable flags. JDK 11–14 also needed `UnlockExperimentalVMOptions`. From JDK 23, `UseZGC` is generational by default; from 24, `-ZGenerational` no longer selects the old collector.

> [!warning] “Pauses under 10 ms” is the old JEP 333 goal, not the current spec
> Reciting 10 ms as what ZGC *is* mixes an early target with the HotSpot guide’s **millisecond** pauses. It is still not zero pause and not a hard SLA. A too-small heap causes allocation stalls while the concurrent cycle tries to free space.

> [!warning] Java 21 `UseZGC` is not generational
> On 21 you need `-XX:+ZGenerational` for young/old. Copying a 24 command line onto 21 silently gets the single-generation collector. ZGC is never the SE default; vendor “low-latency defaults” are not HotSpot ergonomics ([[How would you explain tuning garbage collector settings on the JVM]]).

> [!tip] Interview answer
> **ZGC is HotSpot’s concurrent compacting collector for tiny pauses on heaps from hundreds of megabytes to 16 TB — you turn it on with `UseZGC`; G1 remains the default.** Colored pointers and load barriers let it relocate objects while the application runs, so pause time tracks roots, not heap size. In Java 21 generational mode is `-XX:+ZGenerational`; later JDKs make that the only mode. Do not quote the original 10 ms JEP goal as the product contract, and do not treat ZGC as Shenandoah with a different flag.
