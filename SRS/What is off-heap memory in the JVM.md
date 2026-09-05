<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/NIO #SRS

# What is off-heap memory in the JVM?

> [!abstract] Short answer
> **Off-heap** memory is storage **outside the Java object heap** — not managed as ordinary GC-collected Java objects. Direct **`ByteBuffer.allocateDirect`** buffers **may reside outside** the garbage-collected heap so native I/O can avoid copies. JDK 21 also describes **native `MemorySegment`s** (Foreign Function & Memory, **preview**) allocated from an **arena** you close. Thread stacks, Metaspace, and the code cache are native too, but they are **VM** pools, not NIO direct buffers — [[What JVM runtime memory regions exist]], [[What is Metaspace and how does it differ from PermGen]].

## Outside `-Xmx`, still inside the process

The Java heap holds **class instances and arrays** and is reclaimed when objects are unreachable. Off-heap memory is **outside** that heap. It is **not** collected just because nothing in Java refers to the bytes; you (or a **cleaner** / **arena**) must **deallocate** it.

**Direct `ByteBuffer`.** `allocateDirect(capacity)` creates a **direct** buffer: the VM tries to run native I/O **on that memory** without copying through an intermediate heap buffer. Direct buffers typically cost more to allocate and free. Contents **may** live outside the GC heap, so they can inflate **process RSS** without showing up as Java-heap used. Prefer them for **large, long-lived, I/O-bound** buffers, and only when you measure a gain. Mapped files and JNI can also produce direct buffers. Cap NIO direct allocations with `-XX:MaxDirectMemorySize` (if unset, the VM picks a limit). OpenJDK throws `OutOfMemoryError: Cannot reserve … bytes of direct buffer memory` after trying reference processing and `System.gc()` to run **Cleaners**.

**FFM (JDK 21 preview).** A **native** `MemorySegment` is backed by an off-heap region. An **arena** decides **when** that region is freed — unlike heap objects, unused off-heap is **not** GC’d automatically.

**Other native.** Class metadata (**Metaspace**), **thread stacks** (`-Xss`), JIT **code cache**, and JNI/`malloc` are also off the object heap. `-XX:NativeMemoryTracking` (default **off**) reports JVM-subsystem native use (heap, class, code, thread). It does **not** make off-heap a second Java heap.

```java
import java.nio.ByteBuffer;

public final class DirectOffHeap {
    public static void main(String[] args) {
        ByteBuffer direct = ByteBuffer.allocateDirect(64 * 1024);
        ByteBuffer heap = ByteBuffer.allocate(64 * 1024);
        System.out.println(direct.isDirect() + " " + heap.isDirect());
    }
}
```

**Listing 1.** `allocateDirect` vs heap-backed `allocate`. The `ByteBuffer` **object** is still on the Java heap; only the **payload** of a direct buffer may be off-heap.

```d2
direction: down
proc: "OS process RSS" {
  width: 240
  height: 40
}
jheap: "-Xmx Java heap\nobjects, arrays" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
off: "Off-heap / native" {
  width: 300
  height: 90
  style.fill: "#fff8e1"
  nio: "NIO direct buffers" { width: 200; height: 36 }
  vm: "Metaspace, stacks, code" { width: 220; height: 36 }
}
proc -> jheap
proc -> off
```

**Fig. 1.** Off-heap is everything outside the GC-managed object heap. Direct buffers are one application-visible slice; VM native pools are another.

> [!warning] A “full” Java heap is the wrong meter
> Direct-buffer native memory is limited by **`MaxDirectMemorySize`**, not `-Xmx`. You can get `OutOfMemoryError` for **direct buffer memory** while the object heap still has room. Holding the `ByteBuffer` (or a slice) **reachable** prevents Cleaners from unreserving that native memory.

> [!warning] Off-heap is not “untracked magic”
> NIO direct capacity is accounted in `Bits` / `MaxDirectMemorySize`. JVM internals can be watched with **NMT**. Off-heap still is **not** scanned like Java objects: a native leak or a forgotten arena/`ByteBuffer` grows **RSS** until the cap or the OS fails.

> [!tip] Interview answer
> Off-heap means native memory outside the GC heap. The usual API is `ByteBuffer.allocateDirect`, sized separately with `MaxDirectMemorySize`; the buffer object is on-heap, the bytes often are not. FFM arenas (preview in 21) let you free native segments explicitly. Metaspace and thread stacks are also native, but they are VM regions, not a general application cache.
