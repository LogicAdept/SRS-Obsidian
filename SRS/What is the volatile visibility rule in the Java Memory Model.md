<!--
reps: 0
priority: 0
-->

#Java/JMM #Java/Language/Modifiers/Volatile #SRS

# What is the volatile visibility rule in the Java Memory Model

> [!abstract] Short answer
> **A write to a volatile variable synchronizes-with all subsequent reads of that variable by any thread (JLS 17.4.4), so a volatile write happens-before every subsequent volatile read (JLS 17.4.5).** Reading the flag publishes all plain writes the writer made before the store — not just the flag itself.

"Subsequent" is defined in the synchronization order, not in wall-clock time: a read that observes the volatile variable's new value is subsequent and receives the edge. The rule makes one volatile flag a cheap publication channel for an entire payload — the writer's earlier plain writes become visible the moment the reader sees the flag ([[What does volatile on a reference field guarantee for visibility]]). Writes and reads of volatile fields behave like monitor exit and entry in memory-ordering terms, but without blocking or mutual exclusion — concurrent volatile writes are still lost updates unless the operation is a single atomic access ([[How would you explain the volatile field modifier in Java]]).

```d2
direction: right
w: "T1: config = new Config()\n(plain write)" {
  width: 285
  height: 104
  style.fill: "#e3f2fd"
}
vw: "T1: ready = true\n(volatile write, release)" {
  width: 285
  height: 104
  style.fill: "#fff3e0"
}
vr: "T2: ready == true\n(volatile read, acquire)" {
  width: 276
  height: 104
  style.fill: "#fff3e0"
}
r: "T2: reads config\n-> sees fully built object" {
  width: 294
  height: 104
  style.fill: "#e8f5e9"
}
w -> vw: "program order"
vw -> vr: "synchronizes-with"
vr -> r: "program order"
```

**Fig. 1.** One volatile edge in the middle guarantees the plain object reference is published together with everything written before the flag.

```java
static Config config;          // plain field
static volatile boolean ready; // publication flag

// writer
config = new Config("host", 8080); // plain writes first
ready = true;                      // volatile write: release

// reader
if (ready) {                       // volatile read: acquire
    Config c = config;             // guaranteed non-null, fully initialized
    System.out.println(c.host());
}
```

**Listing 1.** The flag idiom. A reader that sees `ready == true` also sees the fully built `Config`. If the reader sees `false`, it may still race on `config` if it reads it anyway — the guarantee flows only through the flag.

> [!warning] Visibility, not atomicity and not a per-object guarantee
> The edge orders accesses to *that one variable* and everything before the store; it does not make compound actions atomic — `volatile int` still loses increments ([[Why is the Java increment operator not atomic]], [[What is the difference between volatile fields and atomic variables]]). A `volatile` array gives volatile access to the *reference*, not to its elements — element access needs `AtomicIntegerArray`/`VarHandle` ([[How do VarHandle access modes order memory in Java]]). And a volatile write *after* a plain write does not pull that later write into the edge: only writes before the store are published ([[How does volatile visibility differ from atomicity for compound updates]]).

> [!tip] Interview answer
> **A volatile write happens-before every subsequent read of the same variable: the write is a release, the read an acquire. Practically, when a thread sees the new volatile value, it also sees every plain write the writer did before the store — that is the standard safe-publication idiom. It gives ordering and visibility but not atomicity, and it applies per variable, not per object graph depth.**
