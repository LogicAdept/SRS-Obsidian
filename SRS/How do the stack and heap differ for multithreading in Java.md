<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Concurrency/Threads #SRS

# How do the stack and heap differ for multithreading in Java?

> [!abstract] Short answer
> Each thread has a **private JVM stack** (created with the thread) that holds **frames**: locals, operand stack, partial results. The **heap** is **one** area **shared by all threads**, where **all class instances and arrays** are allocated and later GC’d. Threads share data by putting **references** to heap objects where other threads can load them — not by reading another thread’s frames. A frame “cannot be referenced by any other thread.”

## Private frames vs shared objects

Per-thread areas start when the thread is created and die with it: the **pc** register, the **JVM stack**, and typically a **native method stack** for `native` code. The JVM stack is only pushed/popped as frames; implementations may still **allocate those frames on the heap**. Memory need not be contiguous. Too much stack in one thread → `StackOverflowError`. Failing to create or grow a stack → `OutOfMemoryError`.

The heap is created at VM start. Every `new` instance and every array comes from it. GC reclaims it; you never free objects yourself. Exhausting it → `OutOfMemoryError`. The **method area** (class metadata, bytecode, run-time constant pools) is also shared; the spec even allows it to be logically part of the heap.

A **frame** is created on invoke and destroyed when that invocation completes. Only one frame is current per thread. Locals hold `int`/`float`/`reference`/…; `this` and parameters live there. Operand stack is the per-frame working stack. Other threads: [[Can thread priority reliably control execution order in Java]] does not change this layout. Sharing objects still needs a happens-before — [[Can Java code manually control which thread holds a monitor]].

```java
public final class StackVsHeap {
    static class Box {
        int n;
    }

    static void run(Box shared) {
        int local = 1;          // this thread's frame
        shared.n++;             // heap object, visible in principle to others
        Box tmp = new Box();    // new instance is on the heap; tmp is a local ref
    }
}
```

**Listing 1.** `local` is not another thread’s variable. `shared` and `tmp` are references in this frame; the `Box` objects are on the shared heap. Publishing `tmp` (store into a static, a field another thread reads, etc.) is how the object becomes shared.

```d2
direction: down
t: "Thread T" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
st: "private JVM stack\nframes, locals, operand stack" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
hp: "shared heap\nall instances and arrays" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
t -> st
st -> hp: "references in locals"
```

**Fig. 1.** Two threads each have their own current frame. Both can hold a reference to the **same** heap object. That is the multithreading difference: stack isolation of **frames**, heap sharing of **objects**.

> [!warning] A local variable can still alias shared heap
> Isolation is the **frame**, not “anything the method touches.” Escape `this`, a parameter, or `new` into a static/field/collection and other threads can race on that object. `local++` on an `int` is thread-confined; `shared.n++` is not atomic.

> [!warning] “Stack memory” is not a Java guarantee of off-heap frames
> The VM stack is a **logical** structure. Frames **may be heap allocated**. Do not assume escape analysis, TLAB, or “primitives live only on the stack” as a spec promise. Method metadata is shared, not on your JVM stack.

> [!tip] Interview answer
> Each thread has a private stack of frames (locals and operand stack). The heap is shared: every object and array lives there and is GC’d. Threads don’t read each other’s frames; they share by following references to the same heap objects, which is why those objects need synchronization or immutability. Stack overflow is `StackOverflowError`; a full heap is `OutOfMemoryError`.
