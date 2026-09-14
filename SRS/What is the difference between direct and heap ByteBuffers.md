<!--
reps: 0
priority: 0
-->
#Java/NIO/Buffers #Java/JVM/Memory #SRS

# What is the difference between direct and heap ByteBuffers?

> [!abstract] Short answer
> **`ByteBuffer.allocate(n)` backs the buffer with a Java array on the GC heap; `ByteBuffer.allocateDirect(n)` asks the OS for native memory outside the heap.** The heap buffer costs zero to create and is garbage-collected like any array, but for an I/O syscall the JVM must copy the bytes into a temporary native staging area first. The direct buffer lets the kernel read/write the buffer's memory itself — "it will normally have somewhat higher allocation and deallocation costs" — so the javadoc advice is to use one "only for large, long-lived buffers". Check with `isDirect()`; a direct buffer has **no** backing array ([[What is off-heap memory in the JVM]], [[What is a Buffer in Java NIO and how do position limit and capacity work]]).

## Where the bytes live

A heap `ByteBuffer` wraps `byte[]`. When a channel does I/O on it, the JVM cannot hand a garbage-collected, movable array to the kernel, so it copies the region into native memory for the duration of the syscall — two copies per transfer (in and out). A direct buffer sits in native memory from the start; the kernel reads and writes that memory directly, so the copies disappear and the OS page cache streams through the buffer.

| | `allocate` (heap) | `allocateDirect` (direct) |
| --- | --- | --- |
| Storage | GC heap `byte[]` | native (off-heap) memory |
| `hasArray()` | `true` | `false` (`array()` throws) |
| Creation cost | low | higher (system allocation) |
| Syscall I/O | extra JVM staging copy | kernel uses the buffer directly |
| Release | ordinary GC | GC of the wrapper object triggers cleanup |
| Best for | small, short-lived, pool-local work | large, reused I/O buffers |

The wrapper object itself is tiny and lives on the heap; the native region it controls does **not** count against `-Xmx`. Release happens only when the wrapper becomes unreachable and the cleaner runs — reachability, not scope, governs the native footprint.

```java
import java.nio.ByteBuffer;

class DirectVsHeap {
    public static void main(String[] args) {
        ByteBuffer h = ByteBuffer.allocate(8);
        ByteBuffer d = ByteBuffer.allocateDirect(8);
        System.out.println("heap: isDirect=" + h.isDirect() + " hasArray=" + h.hasArray());
        System.out.println("direct: isDirect=" + d.isDirect() + " hasArray=" + d.hasArray());
        long t0 = System.nanoTime();
        for (int i = 0; i < 100_000; i++) ByteBuffer.allocate(4096);
        long t1 = System.nanoTime();
        for (int i = 0; i < 100_000; i++) ByteBuffer.allocateDirect(4096);
        long t2 = System.nanoTime();
        System.out.printf("100k allocations: heap %.1f ms, direct %.1f ms%n",
                (t1 - t0) / 1e6, (t2 - t1) / 1e6);
    }
}
```

**Listing 1.** Identity checks and the allocation-cost gap:

```text
heap: isDirect=false hasArray=true
direct: isDirect=true hasArray=false
100k allocations: heap 58.4 ms, direct 617.9 ms
```

**Listing 2.** Same size, same count: direct allocation is several times more expensive.

```d2
direction: right
heap: "heap ByteBuffer\nbyte[] on the GC heap" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
stage: "JVM native staging copy" {
  width: 250
  height: 45
  style.fill: "#fff8e1"
}
kernel: "kernel / device" {
  width: 210
  height: 45
  style.fill: "#e8f5e9"
}
direct: "direct ByteBuffer\nnative memory" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
heap -> stage -> kernel
direct -> kernel
```

**Fig. 1.** The heap path pays a staging copy per syscall; the direct path is kernel-visible as-is.

> [!warning] "Direct is faster" is a cost model, not a law
> Allocation of a direct buffer is measurably slower, and for small or throwaway buffers the heap wins. Direct memory is invisible to heap dumps and to `Runtime.totalMemory()`; it is capped separately by `-XX:MaxDirectMemorySize` and overflowing it throws `OutOfMemoryError: Direct buffer memory` — not a `StackOverflow`-style crash you can catch meaningfully. The native region is freed only when the wrapper is garbage-collected; a leaked wrapper pins native memory. And `array()` on a direct buffer throws `UnsupportedOperationException`, so code that expects a backing array must branch on `hasArray()`.

> [!tip] Interview answer
> Heap buffers are GC-heap arrays — cheap to make, GC-managed, but each syscall needs a JVM staging copy. Direct buffers live off-heap; the kernel uses their memory directly, which pays off for large, long-lived I/O buffers, while their allocation is costlier and their release depends on GC of the tiny wrapper object. Rule of thumb from the javadoc: direct only for large, long-lived buffers; check `isDirect()`/`hasArray()`; watch `-XX:MaxDirectMemorySize`.

