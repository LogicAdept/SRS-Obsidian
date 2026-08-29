<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/JVM/GarbageCollector #Java/Exceptions/Error #SRS

# How do you diagnose memory pressure and `OutOfMemoryError`?

> [!abstract] Short answer
> **Start from the detail message, not from “it must be a leak.”** The text after `OutOfMemoryError:` tells you which pool failed (Java heap, Metaspace, compressed class space, native, or an oversize array). Confirm that pool is large enough, then watch whether the **live set after full GC** still grows. Heap dumps and histograms show *what* is retained.

## Read the message, then size, then dump

`OutOfMemoryError` is a `VirtualMachineError`. A reasonable application should not “handle” it and continue ([[What is VirtualMachineError]], [[What is java.lang.Error]], [[Why should you not catch java.lang.Error]]). Diagnosis uses the **detail string** and tooling, not a `catch`.

Typical messages:

- **`Java heap space`** — an object could not be allocated in the heap. Often `-Xmx` (or the default) is too small. In a long-lived process it can also mean retained references (a leak) or a finalizer queue that cannot keep up. Not every heap OOME is a leak.
- **`GC overhead limit exceeded`** — GC is running almost constantly (~98% of time, recovering &lt; 2% for several consecutive collections). Live data barely fits. Increase the heap (or turn the check off with `-XX:-UseGCOverheadLimit` — that hides the symptom).
- **`Metaspace` / `Compressed class space`** — class metadata, not `-Xmx`. Size with `MaxMetaspaceSize` / `CompressedClassSpaceSize`. Growing loaders point at a class-metadata leak ([[What is the difference between PermGen space and Metaspace OutOfMemoryError]]).
- **`Requested array size exceeds VM limit`** — length past the VM’s array-length cap, **regardless of free heap** ([[What is OutOfMemoryError Requested array size exceeds VM limit]], [[How do you reproduce an OutOfMemoryError in Java]]).
- **Native / swap / JNI** — native allocation failed. A heap dump of Java objects will not explain it; use OS native tools.

**Before** calling it a leak, size the pool that the message named (`-Xms`/`-Xmx`, `MaxMetaspaceSize`, …). A leak is unintentional retained references (or classes). The signal is a **live set** (heap or Metaspace used **after a full GC**) that keeps rising under **stable** load. Watch that with JConsole, JDK Mission Control, or GC logs (`-Xlog:gc*`). Full GCs that reclaim almost nothing mean the heap is undersized or retained.

**Heap dumps** are the main Java-heap leak artifact: `jcmd … GC.heap_dump`, `jmap -dump`, JConsole’s `HotSpotDiagnostic` MBean, or `-XX:+HeapDumpOnOutOfMemoryError` (optional `-XX:HeapDumpPath`). Prefer `jcmd` over `jmap`. Histograms (`jcmd … GC.class_histogram`) show growing types. For Metaspace, `jcmd VM.classloader_stats`.

```d2
direction: down
msg: "OOME detail message" {
  width: 280
  height: 50
}
heap: "Java heap / GC overhead" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
meta: "Metaspace / CCS" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
other: "array limit or native" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
follow: "size pool, then live set, then a heap snapshot" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}
msg -> heap
msg -> meta
msg -> other
heap -> follow
meta -> follow
```

**Fig. 1.** The detail message picks the pool. Then check size and live set before assuming a leak.

```text
java -Xmx256m \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=./java_pid%p.hprof \
  -Xlog:gc*:file=gc.log \
  YourApp
```

**Listing 1.** Capture a heap dump on JVM heap exhaustion and GC logs. That dump option applies to **Java heap** exhaustion from the VM, not to `throw new OutOfMemoryError()` in application code or to other resource failures.

> [!warning] `OutOfMemoryError` is not automatically a leak
> Undersized `-Xmx`, a huge array, Metaspace, and native exhaustion all throw the same type with **different** messages.

> [!warning] `-XX:+HeapDumpOnOutOfMemoryError` is not universal
> It dumps when the **Java heap** is exhausted by the JVM. It does not dump for an OOME you construct in Java, or for native-thread / swap-style exhaustion.

> [!tip] Interview answer
> **Read the `OutOfMemoryError` detail message first — heap, Metaspace, array limit, and native are different problems.** Check the pool is sized, then see if the live set after full GC still grows. Heap dumps and histograms show retained objects; do not diagnose by catching `Error` and continuing.
