<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Java/JVM #SRS

# What are Java threads composed of?

> [!abstract] Short answer
> Each JVM thread has **per-thread** run-time data: a **pc register**, a **Java Virtual Machine stack** of **frames**, and typically a **native method stack** (“C stack”). **Shared** across threads: the **heap** and the **method area**. A frame holds **locals**, an **operand stack**, and a link to the class’s **run-time constant pool**. The language also has a **`java.lang.Thread`** object (name, id, daemon, interrupt, `ThreadLocal`s) on the **heap**. Frames: [[How would you explain the JVM stack and stack frames]]. Stack vs heap: [[How do the stack and heap differ for multithreading in Java]]. Frame internals: [[How would you explain what a JVM stack frame represents]]. Native size: [[Which JVM flag controls native thread stack size]]. VTs: [[How would you explain Virtual Threads]].

## Per-thread vs shared

The **pc** is the current bytecode address, **undefined** while the thread runs **native** code. The **JVM stack** is created with the thread, holds frames, is **not** contiguous, and **frames may be heap-allocated**. Too deep → **`StackOverflowError`**; cannot create/expand the stack → **`OutOfMemoryError`**. **Native** stacks support JNI and some interpreters; they can also SOE/OOM. Other threads **cannot reference** a frame.

**Heap**: all objects and arrays (including the `Thread` instance and objects your locals **refer** to). **Method area**: per-class metadata and bytecode (logically heap, shared). **`ThreadLocal`** values live in that thread’s map of heap objects, not in the JVM stack. Platform threads wrap a **large OS stack**; virtual threads are **user-mode** with **few** resources and **carriers** — still the same pc/stack/frame model for Java code.

```java
Thread t = Thread.currentThread(); // heap object: id, name, interrupt, locals
int x = 1;                         // local in the current frame
Object o = new Object();           // o in the frame; Object on the heap
```

**Listing 1.** The `Thread` and `o` are heap. `x` is frame-local. Other threads do not see `x`.

```d2
direction: down
th: "one thread" {
  width: 140
  height: 36
  style.fill: "#fff8e1"
}
pc: "pc" {
  width: 80
  height: 32
  style.fill: "#e3f2fd"
}
js: "JVM stack / frames" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
ns: "native stack" {
  width: 140
  height: 32
  style.fill: "#f3e5f5"
}
hp: "shared heap + method area" {
  width: 220
  height: 36
  style.fill: "#ffebee"
}
th -> pc
th -> js
th -> ns
js -> hp: "references only"
```

**Fig. 1.** Composition is pc + stacks. Objects are not “on the thread”; references in frames point at the heap.

> [!warning] The JVM stack is not the `Thread` object
> `java.lang.Thread` is an ordinary heap object. Killing the object does not exist; the thread **terminates** when `run` completes.

> [!warning] Locals that are references alias the heap
> Sharing `o` is sharing the **object**, not the frame. That still needs a **happens-before**.

> [!tip] Interview answer
> A Java thread is a pc, a JVM stack of frames, and usually a native stack, plus a Thread object on the heap. Frames hold locals and the operand stack and are private. The heap and method area are shared, so objects are not stored in the thread even if a local points at them.
