<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS

# What JVM runtime memory regions exist?

> [!abstract] Short answer
> The spec names **per-thread** areas — the **`pc` register**, a **Java Virtual Machine stack** of **frames**, and optional **native method stacks** — and **shared** areas created at VM start: the **heap** (class instances and arrays) and the **method area** (per-class data, including each **run-time constant pool**). HotSpot then implements the method area as **Metaspace**, JIT machine code in a **code cache**, and extra **native/direct** memory outside `-Xmx` — [[How would you explain the Java stack and heap]], [[How does object memory allocation work]].

## Spec regions (JVMS 2.5)

| Area | Shared? | Holds | Typical failure |
| --- | --- | --- | --- |
| **`pc` register** | Per thread | Address of the current bytecode; **undefined** while a `native` method runs | — |
| **JVM stack** | Per thread | **Frames** (locals, operand stack, link to the class’s run-time constant pool) | `StackOverflowError` if the stack cannot grow; `OutOfMemoryError` if a new stack cannot be created or expanded |
| **Native method stacks** | Per thread (if present) | C-like stacks for `native` code and some interpreters | Same pair of errors |
| **Heap** | Shared | All **class instances** and **arrays**; GC reclaims them | `OutOfMemoryError` |
| **Method area** | Shared | Per-class structures: run-time constant pool, field/method data, bytecode | `OutOfMemoryError` |
| **Run-time constant pool** | Per class, **inside** the method area | Literals and symbolic refs used by bytecodes | `OutOfMemoryError` if the method area cannot hold it |

Frames may be **heap-allocated**; the JVM stack need not be one contiguous native segment. The method area is **logically** part of the heap in the spec, but HotSpot keeps class metadata **out** of `-Xmx` — [[What is Metaspace and how does it differ from PermGen]], [[What is the JVM class constant pool]], [[How would you explain the JVM stack and stack frames]].

```java
public final class RegionsDemo {
    public static void main(String[] args) {
        int n = 42;
        String s = new String("x");
        System.out.println(n + s.length());
    }
}
```

**Listing 1.** `n` and the **reference** `s` live in `main`’s **frame**. The `String` **instance** (and its `char`/`byte` payload) live on the **heap**. The `String` class’s metadata and run-time constant pool live in the **method area**.

```d2
direction: down
thread: "Per thread: pc + JVM stack (+ native stack)" {
  width: 360
  height: 50
  style.fill: "#e3f2fd"
}
shared: "Shared: heap + method area (run-time pools)" {
  width: 360
  height: 50
  style.fill: "#e8f5e9"
}
hs: "HotSpot extras: Metaspace, code cache, direct/native" {
  width: 380
  height: 50
  style.fill: "#fff8e1"
}
thread -> shared: "references, not objects"
shared -> hs: "not JVMS 2.5 names"
```

**Fig. 1.** Interview maps start from JVMS 2.5, then name HotSpot pieces that sit **beside** the Java heap.

## HotSpot pieces interviewers add

- **Metaspace** — native memory for class metadata (the method area after Java 8; PermGen is gone). `-XX:MaxMetaspaceSize` / `-XX:MetaspaceSize`, not `-Xmx`.
- **Java heap layout** — Eden / survivor / old (G1: regions; humongous objects skip Eden) — [[What are garbage collector generations]].
- **Code cache** — JIT-compiled code; capped by `-XX:ReservedCodeCacheSize` (default 240 MB with tiered compilation).
- **Direct / off-heap** — `ByteBuffer.allocateDirect` and similar native allocations; `-XX:MaxDirectMemorySize`. The `ByteBuffer` **object** is still on the Java heap — [[What is off-heap memory in the JVM]].

```text
java -Xms256m -Xmx256m \
  -XX:MaxMetaspaceSize=256m \
  -Xss1m \
  YourApp
```

**Listing 2.** Three different limits: Java object heap (`-Xmx`, same as `-XX:MaxHeapSize`), class metadata native memory (`MaxMetaspaceSize`), per-thread stack (`-Xss`; HotSpot rounds up to a page). Native Memory Tracking `summary` buckets include Java heap, class, code, and thread — process RSS is larger than `-Xmx`. G1 further splits the **object** heap into Eden, survivor, and old regions.

> [!warning] Heap versus stack is not the whole map
> Locals hold **primitives and references**. Primitive **fields** sit **inside** heap objects. Class metadata is the **method area** (Metaspace), not “static fields on the heap” as a complete story — the **variables** are class data; any objects they name are heap instances — [[Is it true that primitives live on the stack and reference instances live on the heap]].

> [!warning] `-Xmx` is not process RSS
> Code cache, Metaspace, thread stacks, direct buffers, and the C heap sit **outside** the Java object heap. Listing only “heap + stack” hides OOME and RSS that `-Xmx` never covers.

> [!tip] Interview answer
> JVMS runtime areas are the per-thread pc, JVM stack, and native stacks, plus a shared heap and method area with per-class run-time constant pools. HotSpot maps the method area to Metaspace and adds a JIT code cache and off-heap native memory. Heap holds instances and arrays; stacks hold frames with references, not the objects themselves.
