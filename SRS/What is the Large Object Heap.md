<!--
reps: 0
priority: 0
-->
#ProgrammingLanguages/CSharp #Java/JVM/Memory/Heap #SRS

# What is the Large Object Heap?

> [!abstract] Short answer
> The **large object heap (LOH)** is a **.NET** GC region for objects whose size is **≥ 85,000 bytes**. They skip generation 0/1, live on **LOH segments** (sometimes nicknamed “generation 3”), and are collected only with a **generation 2** (full) GC. The JVM has **no LOH**. Under G1 the analog is a **humongous object**: size **≥ half a heap region**, allocated as contiguous **old-generation** regions — [[What are garbage collector generations]], [[What JVM runtime memory regions exist]].

## .NET: a separate heap because moving large objects is expensive

The CLR splits the managed heap into the **small object heap (SOH)** and the **LOH**. User code allocates only in **generation 0** or on the **LOH**. Compacting a huge object (copying it) is costly, so the default gen-2 pass **sweeps** the LOH: dead objects become a **free list** for later large allocations; adjacent holes merge. The runtime **may** compact the LOH on its own. To force compaction on the **next full blocking** GC, set `GCLargeObjectHeapCompactionMode.CompactOnce` (it then resets to `Default`). **Background** gen-2 collections are not blocking and **do not** compact.

A large allocation that exceeds the LOH’s threshold triggers a **generation 2** collection of the **whole** heap. Temporary large arrays therefore tax gen 2 even when the SOH is healthy. New LOH memory is **zeroed**; that cost dominates allocation of the smallest large object.

```csharp
using System;
using System.Runtime;

static class LohDemo
{
    static void Main()
    {
        byte[] buffer = new byte[85_000];
        Console.WriteLine(GC.GetGeneration(buffer));

        GCSettings.LargeObjectHeapCompactionMode =
            GCLargeObjectHeapCompactionMode.CompactOnce;
        GC.Collect();
    }
}
```

**Listing 1.** `new byte[85_000]` is a large object (≥ 85,000 bytes). `GetGeneration` reports **2**. `CompactOnce` plus a blocking `GC.Collect()` compacts the LOH once; do not rely on background gen 2 for that.

```d2
direction: down
soh: "Small object heap\ngen 0 → 1 → 2 (compacted)" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
loh: "Large object heap\n≥ 85,000 bytes, collected with gen 2" {
  width: 340
  height: 55
  style.fill: "#fff8e1"
}
g1: "G1 JVM analog: humongous\n≥ ½ region, contiguous old regions" {
  width: 340
  height: 55
  style.fill: "#e8f5e9"
}
soh -> loh: "size threshold"
loh -> g1: "not the same runtime"
```

**Fig. 1.** LOH is a CLR segment, not a Java heap space. G1 still puts oversized objects in the **old generation**, just in **humongous** regions.

## JVM: humongous objects, not an LOH

G1 treats an object as **humongous** when it is **at least half a region**. Region size is ergonomic (about 2048 regions) or `-XX:G1HeapRegionSize` (power of two, 1–512 MB). The object occupies a **contiguous** run of **old** regions, starting at the first region’s start; leftover bytes in the last region stay unused until the object dies. Humongous allocation **bypasses Eden** — [[How does object memory allocation work]]. G1 usually only **marks** them live or dead; it **moves** them only as a last-resort Full GC. Primitive arrays may be **eagerly reclaimed**. A humongous allocation can trip IHOP and start concurrent marking. Lack of **contiguous** regions can fail with `OutOfMemoryError` even when free heap exists.

> [!warning] The JVM does not have a Large Object Heap
> **LOH** is a **.NET** name and an **85,000-byte** cutoff. Do not map it onto `-Xmx` or Eden. Interview answers that say “Java’s LOH” are mixing runtimes. Say **humongous object** (G1) or “allocated in old” for other collectors.

> [!warning] Default LOH collection does not compact
> Sweeping leaves **holes**. Churn of temporary large arrays fragments the LOH and can force extra **full** GCs. `CompactOnce` applies to the **next blocking** gen-2 collection only. Microsoft’s LOH write-up is **Windows**-centric (VirtualAlloc/VirtualFree); other OS ports exist but that page does not define them.

> [!tip] Interview answer
> The Large Object Heap is the .NET GC’s area for objects of 85,000 bytes or more; they are collected with generation 2 and are swept rather than compacted unless you request CompactOnce. The JVM has no LOH: under G1, objects at least half a region are humongous, live in contiguous old regions, and barely move. Do not treat 85 kilobytes as a HotSpot threshold.
