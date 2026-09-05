<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is Shenandoah GC?

> [!abstract] Short answer
> **An OpenJDK low-pause collector that *evacuates/compacts concurrently* with mutator threads.** Pause times are meant to stay short and **independent of heap size** (same idea at 200 MB or 200 GB). Enable with `-XX:+UseShenandoahGC`. It is **not** in Oracle’s Java 21 GC catalog; many OpenJDK builds ship it. Production (no experimental unlock) from JDK 15.

## Concurrent compact, not “ZGC with another name”

JEP 189 (experimental in **JDK 12**): Shenandoah shortens pauses by doing **evacuation work concurrently**. G1 does not concurrent-evacuate; CMS marks concurrently but **never compactes old**. Shenandoah adds an **indirection pointer** on every object so GC threads can compact the heap while Java threads run. **Marking and compacting** are concurrent; STW is only long enough to **scan (and later update) roots** on thread stacks — so pause length tracks the **root set**, not live-set size.

JEP 379 (**JDK 15**): product feature. `-XX:+UnlockExperimentalVMOptions` is no longer required with `-XX:+UseShenandoahGC`. It does **not** become the default collector (that stays G1).

It trades **CPU and extra heap** for those pauses. It is a regionalized collector (heap as regions). It is **not** the same algorithm as ZGC (ZGC uses colored pointers and load/store barriers; Shenandoah uses a per-object **indirection / forwarding** pointer). Both aim at low, heap-size-independent pauses ([[What is ZGC]], [[What is G1 GC]], [[What is CMS Concurrent Mark Sweep GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

Availability is a **build** question. Oracle’s Java 21 `java` man page and Available Collectors list Serial, Parallel, G1, and ZGC — not Shenandoah. OpenJDK/Temurin/Corretto-style binaries often include it; Oracle JDK historically does not. Builds can disable it with `--with-jvm-features=-shenandoahgc`. If `UseShenandoahGC` is unrecognized, you do not have that collector ([[How does garbage collection work on the JVM]]).

JDK 12–14 needed the experimental unlock. Degenerated or Full GC still exists if allocation outruns the concurrent cycle — low pause is the *concurrent* path, not a hard SLA.

```d2
direction: down
g1: "G1: concurrent mark\nSTW evacuate" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
sh: "Shenandoah: concurrent mark\n+ concurrent evacuate" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
pause: "STW ≈ root scan/update\nnot heap size" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
g1 -> sh: "the missing piece"
sh -> pause
```

**Fig. 1.** The JEP’s contrast with G1: Shenandoah moves objects while the application runs. Pauses remain for roots.

```text
# JDK 15+ OpenJDK build that actually includes Shenandoah
java -XX:+UseShenandoahGC -Xlog:gc YourApp

# JDK 12–14 (experimental)
java -XX:+UnlockExperimentalVMOptions -XX:+UseShenandoahGC YourApp
```

**Listing 1.** If the VM rejects `UseShenandoahGC`, this is an Oracle-style or `--without-shenandoahgc` binary — switch collector or switch JDK flavor. Not a tuning miss.

> [!warning] Not on Oracle JDK 21
> Reciting Shenandoah next to G1/ZGC as if every `java` has it fails interviews against Oracle’s own 21 guide. Check `-XX:+UseShenandoahGC -version` on the actual runtime.

> [!warning] “Like ZGC” is the wrong algorithm
> Same *goal* (short pauses, big heaps). Different *mechanism* (forwarding vs colored pointers). ZGC is in the Oracle 21 catalog; Shenandoah often is not.

> [!tip] Interview answer
> **Shenandoah is OpenJDK’s concurrent-compacting collector: it copies live objects while the app runs, so pauses stay short even on huge heaps.** Enable it with `UseShenandoahGC` (experimental unlock until JDK 15). It is not in Oracle JDK’s usual collector set; G1 remains the default. Do not describe it as ZGC with a different flag.
