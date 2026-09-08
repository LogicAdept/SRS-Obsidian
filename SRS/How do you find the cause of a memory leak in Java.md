<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/JVM/Tuning #SRS

# How do you find the cause of a memory leak in Java?

> [!abstract] Short answer
> A leak is **unintentionally retained** heap or class metadata. Confirm the signal first — a **live set after full GC that keeps rising** under stable load — then capture **heap dumps** (`jcmd <pid> GC.heap_dump`, or `-XX:+HeapDumpOnOutOfMemoryError` with `-XX:HeapDumpPath`) and compare two dumps taken minutes apart: the objects that only grow are the leak. In the analyzer, open the **dominator tree** and follow the **path to GC roots** from the biggest keeper to the field that pins it — [[How do you diagnose memory pressure and OutOfMemoryError]], [[How do you capture a Java heap dump]].

## The usual suspects

- **Unbounded caches and static collections** — a `static Map` used as a cache with no eviction keeps every key until the process dies. Fix: bounded/weak caches with a real eviction policy.
- **`ThreadLocal` not cleaned in pooled threads** — a pool keeps threads alive forever, so a `ThreadLocal` value set per task stays reachable from that thread. Call `ThreadLocal.remove()` when the task is done (the javadoc contract: it removes the current thread's value and reinitializes on next read).
- **Unclosed resources** — streams, connections, cursors registered with native memory; use try-with-resources ([[What forms of try catch and try with resources exist in Java]]).
- **Listeners and callbacks on long-lived objects** — registered once, never removed; the long-lived holder pins the listener and everything it references.
- **Classloader leaks** — in containers/app servers, a stale driver, `ThreadLocal`, or listener pins the application classloader, so **every loaded class stays resident**; this shows up as `OutOfMemoryError: Metaspace` growth, checked with `jcmd <pid> VM.classloader_stats`. Before JDK 8 this lived in the **permanent generation** — removed by JEP 122, so "increase PermGen" is legacy advice ([[What is Metaspace and how does it differ from PermGen]]).

```bash
jcmd <pid> GC.heap_info                 # live set per pool, at a glance
jcmd <pid> GC.class_histogram           # who grows between two runs
jcmd <pid> GC.heap_dump /tmp/d1.hprof   # dump 1
jcmd <pid> GC.heap_dump /tmp/d2.hprof   # dump 2, minutes later — compare
```

**Listing 1.** Terminal workflow: watch the live set, find the growing types, then take two dumps and diff them in a heap analyzer. `GC.heap_dump` forces a full GC first (add `-all` to skip that and include unreachable objects).

```d2
direction: down
signal: "Live set grows after full GC" {
  width: 300
  height: 52
  style.fill: "#fff8e1"
}
dump: "Two heap dumps (minutes apart)" {
  width: 320
  height: 52
  style.fill: "#e3f2fd"
}
tree: "Dominator tree\nbiggest retained keepers" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
path: "Path to GC roots\nwhich field pins it" {
  width: 300
  height: 52
  style.fill: "#fce4ec"
}
fix: "Fix: eviction / ThreadLocal.remove /\nclose, deregister" {
  width: 340
  height: 60
  style.fill: "#e8f5e9"
}
signal -> dump -> tree -> path -> fix
```

**Fig. 1.** From symptom to culprit: confirm growth, diff dumps, rank keepers, trace the pinning reference, then fix the holding code.

> [!warning] Do not start by "optimizing" the JVM flags
> Raising `-Xmx` makes a leak **slower to notice**, not gone — the process just reaches the bigger ceiling later. Also, one heap dump shows *what* is big, not necessarily *what leaks*; a single dump can even catch short-lived allocation churn. The leak is the **delta** between dumps — [[How do you reproduce an OutOfMemoryError in Java]].

> [!tip] Interview answer
> First I prove it is a leak: live set after full GC keeps climbing under stable load. Then I capture heap dumps — `jcmd GC.heap_dump` twice, or automatically on `OutOfMemoryError` — and diff them. In the analyzer I sort the dominator tree by retained heap and walk the path to GC roots to find the field that pins the objects. Typical culprits: unbounded caches, `ThreadLocal` values in pooled threads, unclosed resources, forgotten listeners, and classloader leaks that surface as Metaspace growth.
