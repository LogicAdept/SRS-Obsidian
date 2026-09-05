<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory/Heap #Java/Concurrency/Threads #SRS

# How do you reproduce an `OutOfMemoryError` in Java?

> [!abstract] Short answer
> **Fill the pool the message names.** Keep allocating Java objects that stay reachable under a small `-Xmx` for **`Java heap space`**. Other recipes (oversize array length, tiny Metaspace, many threads, NIO direct buffers) throw the same `Error` type with **different** detail text. `throw new OutOfMemoryError()` does not exhaust the VM.

## Match the recipe to the detail message

`OutOfMemoryError` is a `VirtualMachineError`. The JVM throws it when an allocation cannot be satisfied: class instance or array creation, boxing, class init, or (asynchronously) some resource limits ([[What is VirtualMachineError]], [[How would you explain OutOfMemoryError]], [[How do you diagnose memory pressure and OutOfMemoryError]]).

**`Java heap space`:** retain objects so GC cannot free them. A static `List`/`Map` that keeps growing `byte[]` chunks under `-Xmx16m` is enough. That is the leak-shaped case (unintentional retained references), not a bigger array than the VM will ever allow. A legal but huge array such as `new Integer[1_000_000_000]` under a tiny heap is usually this message too, **not** `Requested array size exceeds VM limit` ([[What is OutOfMemoryError Requested array size exceeds VM limit]]).

**`Requested array size exceeds VM limit`:** ask for a length past this VM’s max array size. Raising `-Xmx` does not fix it.

**`Metaspace`:** class metadata lives in native Metaspace, not `-Xmx`. Bound it with `MaxMetaspaceSize` and load or generate **many** classes. Bytecode libraries are one way to generate types; they are not required to understand the pool ([[What is the difference between PermGen space and Metaspace OutOfMemoryError]]).

**Native threads:** the VM can throw `OutOfMemoryError` on **native thread creation**, separate from Java-heap exhaustion (`-XX:+HeapDumpOnOutOfMemoryError` does not dump for that). Each platform thread has a native stack (`-Xss`; the default size is platform-specific, not a fixed 1 MB). Creating threads in a loop until start fails is the usual stress. That is not `StackOverflowError` ([[How do you produce a StackOverflowError]]).

**NIO direct buffers:** `ByteBuffer.allocateDirect` memory may sit **outside** the GC heap. `-XX:MaxDirectMemorySize` caps total `java.nio` direct-buffer allocations. Looping `allocateDirect` with a small cap stresses that pool, not `-Xmx`.

```d2
direction: down
oome: "OutOfMemoryError" {
  width: 260
  height: 40
}
heap: "retain objects, small -Xmx\nJava heap space" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
meta: "many classes, MaxMetaspaceSize" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
other: "VM-limit array / threads / direct NIO" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
oome -> heap
oome -> meta
oome -> other
```

**Fig. 1.** Same type; reproduce the **pool** you care about. Catching `Error` is not a test ([[Why should you not catch java.lang.Error]]).

```java
class Demo {
    static final java.util.List<byte[]> held = new java.util.ArrayList<>();

    static void fillHeap() {
        for (;;) {
            held.add(new byte[1_000_000]);
        }
    }
}
```

**Listing 1.** Run with a small `-Xmx`. Objects stay reachable in `held`, so GC cannot reclaim them → typically **`Java heap space`**. Drop the static list and you may never fill the heap.

> [!warning] `new OutOfMemoryError()` is not a reproduction
> That constructs the object. Heap-dump-on-OOME and similar flags apply to **JVM heap exhaustion**, not to an `Error` you throw yourself.

> [!warning] One loop does not cover every message
> A growing `Map` is heap. Threads, Metaspace, direct buffers, and VM-limit array lengths are other pools. A billion-slot array under tiny `-Xmx` is usually **`Java heap space`**, not the VM-limit message.

> [!tip] Interview answer
> **To see `Java heap space`, keep allocating reachable objects under a small `-Xmx` — a static collection that never drops entries is the usual demo.** Other OOMEs need other knobs: Metaspace size, thread native stacks, NIO `MaxDirectMemorySize`, or an array length the VM will not allocate. Do not confuse that with `StackOverflowError`.
