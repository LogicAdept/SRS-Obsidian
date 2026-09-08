<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS

# What are the JVM run-time data areas?

> [!abstract] Short answer
> The JVM spec defines six run-time data areas. **Per thread:** the **pc register** and the **Java Virtual Machine stack** (which holds frames). **Shared by all threads:** the **heap** (all class instances and arrays), the **method area** (per-class structures), and **native method stacks**. Each loaded class also gets a **run-time constant pool**, allocated from the method area. Per-thread areas are created and destroyed with the thread; shared areas live from JVM start-up to JVM exit — [[How would you explain the JVM stack and stack frames]], [[How would you explain the Java stack and heap]].

## Shared vs per-thread

- **Heap** — memory for **all class instances and arrays**, created at start-up, shared. Storage is reclaimed by the garbage collector; objects are never explicitly deallocated. The heap may be fixed or expandable and need not be contiguous. Heap exhaustion throws `OutOfMemoryError` ([[What are garbage collector generations]]).
- **Method area** — per-class structures: the run-time constant pool, field and method data, and the code for methods and constructors. It is **logically part of the heap**, but the spec lets simple implementations skip garbage-collecting or compacting it. HotSpot implements it as **Metaspace** in native memory since JDK 8 — [[What is Metaspace and how does it differ from PermGen]].
- **Run-time constant pool** — one per class or interface: the runtime image of the class file's `constant_pool` table, from numeric literals to method and field references that get resolved on first use — [[What is the JVM class constant pool]].

Per thread:

- **pc register** — one per thread. It holds the address of the bytecode instruction being executed; while the current method is `native`, its value is **undefined**.
- **Java Virtual Machine stack** — one private stack per thread, storing frames. Deeper than permitted → `StackOverflowError`; no memory to create or expand a stack → `OutOfMemoryError` — [[How would you explain StackOverflowError in Java]].
- **Native method stacks** — optional "C stacks" supporting `native` methods; `Unsafe`/JNI calls and JVM internals use them.

```d2
direction: right
shared: "Shared (JVM start-up → exit)" {
  width: 300
  height: 150
  style.fill: "#e3f2fd"
  heap: "Heap\ninstances + arrays" {
    width: 240
    height: 60
  }
  ma: "Method area\nmetadata, code\n(constant pool per class)" {
    width: 240
    height: 60
  }
}
t1: "Thread A" {
  width: 220
  height: 100
  style.fill: "#e8f5e9"
  pc: "pc register" {
    width: 170
    height: 40
  }
  st: "JVM stack (frames)" {
    width: 180
    height: 40
  }
}
t2: "Thread B" {
  width: 220
  height: 100
  style.fill: "#e8f5e9"
  pc2: "pc register" {
    width: 170
    height: 40
  }
  st2: "JVM stack (frames)" {
    width: 180
    height: 40
  }
}
t1.st -> shared.heap: "references"
t2.st -> shared.heap: "references"
```

**Fig. 1.** Heap and method area are shared; every thread carries its own pc register and frame stack. Constant pools are per class, allocated from the method area.

> [!warning] "Method area is a heap region" is only half true
> The spec says the method area is *logically* part of the heap, but it also says implementations may choose where it lives and whether it is garbage-collected. In HotSpot it is **Metaspace in native memory**, not `-Xmx` space — sizing it with `-Xmx` does nothing, and class-metadata leaks show up as `OutOfMemoryError: Metaspace`, not `Java heap space` — [[How do you diagnose memory pressure and OutOfMemoryError]].

> [!tip] Interview answer
> Six areas: per-thread pc register and JVM stack of frames; shared heap for all instances and arrays; shared method area holding per-class metadata, method code, and each class's run-time constant pool; plus optional native method stacks. Stack overflow is `StackOverflowError`; running out of heap or method-area memory is `OutOfMemoryError`. In HotSpot the method area is Metaspace in native memory since JDK 8.
