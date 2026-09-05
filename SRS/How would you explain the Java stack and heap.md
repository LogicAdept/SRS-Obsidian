<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/JVM/Memory/Stack #SRS

# How would you explain the Java stack and heap?

> [!abstract] Short answer
> The **heap** is the shared run-time area where **every class instance and array** is allocated and later reclaimed by GC. Each thread has a private **Java Virtual Machine stack of frames**. A frame holds **local variables**, an **operand stack**, and a **link** to that class’s run-time constant pool — including **references** into the heap, not the objects themselves. Method return (or an uncaught throw) **destroys the frame**. Other threads see heap objects only through **published references**, never by reaching into another thread’s locals. The full map is larger than these two areas — [[What JVM runtime memory regions exist]], [[How would you explain the JVM stack and stack frames]].

## Shared heap, per-thread frames

**Heap (shared, VM lifetime).** Created at start-up. Memory for all class instances and arrays comes from here. Instance fields live **in the object**, so a `Box.n` or a `Box.next` sits on the heap with that `Box`. There is no explicit free; a garbage collector reclaims storage. If the collector cannot make enough heap available: `OutOfMemoryError` (HotSpot’s usual detail for that pool is `Java heap space`, not the only possible detail). Size is typically `-Xms` / `-Xmx`. The heap need not be one contiguous block — [[How does object memory allocation work]], [[How would you explain OutOfMemoryError]].

**Java Virtual Machine stack (per thread).** Created with the thread and destroyed when the thread ends. It is only pushed and popped as **frames** (call/return is LIFO). A frame is created on invoke and destroyed when that invocation completes, normally or abruptly. Locals can hold primitives or `reference` values; `long`/`double` occupy two local slots. The operand stack holds partial results the same way. The frame does **not** contain the run-time constant pool; it holds a **reference** to the pool, which lives in the **method area**. A frame is **local to its thread** and cannot be referenced by another thread.

References also live in **instance fields**, **array components**, and **class variables** — not only in stack frames. Class variables are not per-frame storage.

The spec stack is not a C array you index. Because it is only used to push and pop frames, **frames may be heap-allocated**. Overflow of the permitted stack → `StackOverflowError`; failing to **create or expand** a stack → `OutOfMemoryError` — [[How would you explain StackOverflowError in Java]]. Native/`C` stacks for `native` methods are a **separate** optional area. Typical HotSpot `-Xss` is on the order of 1 MB per thread (for example 1024 KB default on Linux/x64, rounded to a page). That ratio to `-Xmx` is **configuration**, not a language rule. Allocation “speed” is not in the spec; HotSpot heap allocation is often a TLAB pointer bump.

Do not recite “primitives on the stack, objects on the heap.” A primitive **instance field** is on the heap; a local **reference** is in the frame — [[Is it true that primitives live on the stack and reference instances live on the heap]].

```java
final class StackAndHeap {
    static final class Box {
        int n;
        Box next;
    }

    static int count;

    public static void main(String[] args) {
        int local = 1;
        Box box = new Box();
        box.n = local;
        box.next = null;
        count = 1;
    }
}
```

**Listing 1.** `local` and the `box` **reference** live in `main`’s frame. The `Box` instance, `n`, and `next` live on the heap. `count` is a class variable (method area / class metadata), not a heap instance field and not a local. Another thread cannot read `local`; it can share the `Box` only if this thread **publishes** the reference.

```d2
direction: right
thread: "One thread" {
  width: 260
  height: 130
  style.fill: "#fff8e1"
  frame: "Frame\nlocals + operand stack\n+ link to constant pool" {
    width: 240
    height: 70
  }
}
heap: "Shared heap" {
  width: 240
  height: 130
  style.fill: "#e3f2fd"
  obj: "Box instance\nn, next" {
    width: 200
    height: 55
  }
}
thread.frame -> heap.obj: "reference"
```

**Fig. 1.** The frame stores the pointer. The object and its fields are on the shared heap.

> [!warning] Stack versus heap is not the whole runtime
> The spec also has a per-thread `pc`, optional native method stacks, and a shared **method area** (bytecodes, field/method data, run-time constant pools). HotSpot class metadata is **Metaspace**, outside `-Xmx`. A class **instance** is on the heap; the metadata table is not “the heap.”

> [!warning] A local variable is not “the object on the stack”
> Locals and the operand stack hold **values** (including references). The instance those references denote is on the **heap**. The JVM stack may itself be implemented with heap-allocated frames. Shared heap does **not** mean every object is globally visible — only a published reference is.

> [!warning] Stack full is not only `StackOverflowError`
> Depth past the permitted stack → `StackOverflowError`. If the VM **cannot allocate** a stack (or expand one), that is `OutOfMemoryError`. Heap exhaustion is `OutOfMemoryError` with a **detail** that names the pool.

> [!tip] Interview answer
> Heap is shared and holds every object and array; GC reclaims it and `-Xmx` sizes it. Each thread has a JVM stack of frames with locals, an operand stack, and a link to the class constant pool — including references, not the objects. When the method ends the frame is gone; the object stays until it is unreachable. Primitive fields still live in the heap object, class metadata is a third area, objects are not global, and the stack is not “always faster.”
