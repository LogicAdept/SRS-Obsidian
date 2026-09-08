<!--
reps: 0
priority: 0
-->
#Java/JVM/Tuning #Java/JVM/Memory #Java/Concurrency/Threads #SRS

# What is a heap dump and a thread dump?

> [!abstract] Short answer
> Two different **point-in-time snapshots** for two different classes of failure. A **heap dump** is a capture of the **whole object heap**: every object, its class, field values and the reference graph between objects — the artifact for memory-leak and footprint analysis. A **thread dump** is a capture of **every thread's stack** — frames with class, method, byte-code index and line number, plus thread state and monitor ownership — the artifact for hangs, deadlock and contention. Practical defaults on Java 21: heap — `jcmd <pid> GC.heap_dump` and `-XX:+HeapDumpOnOutOfMemoryError`; threads — `jcmd <pid> Thread.print` or `jstack <pid>`. Both are anatomy for diagnosis: [[How do you capture a Java heap dump]] and [[How do you diagnose memory pressure and OutOfMemoryError]] walk the follow-up steps.

## Heap dump: the object graph frozen

A heap dump answers *"who holds the memory?"*. It contains all live objects with their types and field values, arrays with contents, and class metadata — everything needed to rebuild the **dominator tree** and find the shortest reference path from a root to a leaking object. Capture is available in three verified ways:

* **On demand:** `jcmd <pid> GC.heap_dump <file>` — the JDK 21 `jcmd` reference documents options `-all` ("Dump all objects, including unreachable objects"), `-gz` (gzip with compression level 1–9) and `-overwrite`.
* **On `OutOfMemoryError`:** the `java` launcher documentation defines **`-XX:+HeapDumpOnOutOfMemoryError`** — "Enables the dumping of the Java heap to a file in the current directory ... when a `java.lang.OutOfMemoryError` exception is thrown" — with **`-XX:HeapDumpPath=...`** to choose the location. This is the flag you set in production **before** the incident.
* The result is the binary **HPROF** format, understood by Eclipse MAT, VisualVM and similar analyzers.

## Thread dump: every stack, with locks

A thread dump answers *"who is stuck, on what, waiting for whom?"*. Per the `jstack` command reference, it "prints Java stack traces of Java threads for a specified Java process" and "for each Java frame, the full class name, method name, byte code index (BCI), and line number, when available, are printed" — together with each thread's state and the monitors it holds or waits for. The equivalent modern invocation is **`jcmd <pid> Thread.print`** ("Prints all threads with stacktraces" per the `jcmd` reference). A dump taken during a hang shows blocked chains like *A holds lock X, B waits for X*, and deadlock detection marks cycles where several threads wait on each other — the entry point for analyzing [[How can a servlet deadlock]].

```java
// Capture commands (run against a running JVM, <pid> from jps):
//   jcmd <pid> Thread.print                        // thread dump to stdout
//   jstack <pid> > threads-1.txt                   // same via jstack
//   jcmd <pid> GC.heap_dump /tmp/hprof.hprof       // binary heap snapshot
//   jcmd <pid> GC.heap_dump -all /tmp/full.hprof   // include unreachable objects
// JVM flags for automatic capture:
//   -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp
```

**Listing 1.** The four invocations worth knowing from memory; the flags belong in every production JVM configuration.

```d2
direction: right
symptom: "Symptom" {
  leak: "memory grows,\nGC cannot reclaim" {style.fill: "#ffebee"}
  hang: "requests hang,\nCPU or threads stuck" {style.fill: "#ffebee"}
}
tool: "Capture" {
  heapdump: "jcmd GC.heap_dump\nor HeapDumpOnOutOfMemoryError" {style.fill: "#e3f2fd"}
  threaddump: "jcmd Thread.print\nor jstack" {style.fill: "#e3f2fd"}
}
artifact: "Analyze" {
  mat: "HPROF file:\ndominator tree, paths to roots" {style.fill: "#e8f5e9"}
  stacks: "stacks + monitor owners:\nblocked chains, deadlocks" {style.fill: "#e8f5e9"}
}
leak -> heapdump -> mat
hang -> threaddump -> stacks
```

**Fig. 1.** Symptom decides the snapshot: object graph questions go to a heap dump, scheduling questions go to a thread dump.

## When each one pays off

A single thread dump is a photo; a **series** of dumps a few seconds apart is a film — one blocked stack can be a coincidence, three identical ones are a diagnosis. Thread dumps are cheap and safe enough for production on every incident. Heap dumps are the opposite: freezing a multi-gigabyte heap takes time and disk, so they are either taken on `OutOfMemoryError` (where the JVM is already dying) or deliberately during a maintenance window. For sizing and pool questions the dump is often the second stop after understanding [[Which states can a Java thread be in]].

> [!warning] `jstack` and `jmap` are officially unsupported
> Both man pages carry the note "**This command is experimental and unsupported**", and `jmap` adds that it "might not be available in future releases of the JDK". The supported front door is **`jcmd`** (`Thread.print`, `GC.heap_dump`). A second trap: a heap dump taken while the JVM is still serving traffic can pause it for seconds and produce a file as large as the heap — know your `-XX:HeapDumpPath` disk budget before the incident, not during it.

> [!tip] Interview answer
> **A heap dump is a full snapshot of the object heap — every object, class and reference — captured via jcmd GC.heap_dump or automatically with -XX:+HeapDumpOnOutOfMemoryError, and read in MAT to find leaks by dominator tree and paths to roots. A thread dump is a snapshot of all thread stacks with states and monitor ownership, taken via jcmd Thread.print or jstack, and used to diagnose hangs, contention and deadlocks. Heap dumps answer who holds memory; thread dumps answer who is blocked on whom.**
