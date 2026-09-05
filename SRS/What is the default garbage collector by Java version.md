<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/Versions #SRS

# What is the default garbage collector by Java version?

> [!abstract] Short answer
> **It is ergonomic, not a single name per marketing number.** Java 8: **Parallel (throughput)** on server-class machines (2+ CPUs and 2+ GB RAM), **Serial** otherwise. JDK **9**: **G1** on server configurations (JEP 248). Through Java **21**, G1 is the usual default; **Serial** still wins on some small/single-CPU boxes. JDK **27**: G1 always, even there (JEP 523). ZGC and Shenandoah are never the HotSpot default.

## What the VM picks when you pass no GC flag

HotSpot chooses a collector from **hardware and OS**, then you can override with `-XX:+UseSerialGC`, `UseParallelGC`, `UseG1GC`, `UseZGC`, or (on builds that include it) `UseShenandoahGC`.

| JDK | Default if you specify nothing |
| --- | --- |
| **8** (HotSpot ergonomics) | **Throughput / Parallel** on a **server-class** machine: ≥2 physical processors and ≥2 GB RAM. **Serial** on other setups (and Serial is the documented default on some OS/hardware combos). “Java 8 = Parallel” is the **server** story, not a 1-CPU box. |
| **9** | **G1** on 32- and 64-bit **server** configurations (JEP 248). Parallel had been that server default. Constrained boxes (historically **1 CPU** or **< 1792 MB** RAM) kept **Serial** because G1 lost on throughput/footprint there (JEP 523’s account of the JDK 9 policy). |
| **15–21** | **G1** on most hardware/OS configs (Java 21 guide and `java` man page). Serial still the ergonomic pick on **certain** small configurations. ZGC and Shenandoah exist as **opt-in**; making Shenandoah a product GC explicitly did **not** change the default (JEP 379). |
| **27** | **G1 always** when no collector is set, including those constrained environments (JEP 523). Serial remains available if you ask for it. |

So the dump line “8 = Parallel, 9+ = G1” is the **server** timeline, not a universal law. Check the actual VM with `-XX:+PrintCommandLineFlags` (prints ergonomic GC and heap flags) ([[What is G1 GC]], [[What is Parallel GC]], [[What is Serial GC]], [[What is ZGC]], [[What is Shenandoah GC]]).

No OpenJDK JEP makes ZGC or Shenandoah the default. Vendor builds that change defaults are not “the Java default.”

```d2
direction: right
j8: "JDK 8\nParallel if server-class\nelse Serial" {
  width: 200
  height: 70
  style.fill: "#fff8e1"
}
j9: "JDK 9–26\nG1 on servers\nSerial if tiny" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
j27: "JDK 27\nG1 always" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
j8 -> j9
j9 -> j27
```

**Fig. 1.** Default collector follows machine class, then G1 takes over servers in 9, then everyone in 27.

```text
java -XX:+PrintCommandLineFlags -version
```

**Listing 1.** Shows whether this process actually got `UseG1GC`, `UseParallelGC`, or `UseSerialGC`. Do not recite a slide; print the flags on the JDK you ship ([[How does garbage collection work on the JVM]], [[How would you explain tuning garbage collector settings on the JVM]]).

> [!warning] “Java 8 = Parallel, Java 9+ = G1” fails on small machines
> A 1-CPU or sub-2 GB box on 8 is Serial. The same class of box can still be Serial on 21. Only JDK 27’s JEP 523 makes “always G1” true for vanilla HotSpot.

> [!warning] Latency collectors are not the default
> ZGC and Shenandoah are flags you set. They are not what `java YourApp` uses on Oracle/OpenJDK unless a vendor changed that — and that is not the SE default.

> [!tip] Interview answer
> **On servers, Parallel was the default through 8 and G1 from 9; Serial is the small-machine collector until 27, when G1 is always default.** Always say “ergonomics,” not a single name per version. ZGC/Shenandoah are opt-in. Confirm with `PrintCommandLineFlags` on the actual JDK.
