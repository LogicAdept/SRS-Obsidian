<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Stack #SRS

# How would you explain what a JVM stack frame represents?

> [!abstract] Short answer
> A **frame** is the VM’s record of **one method invocation** on one thread. It stores that call’s **data and partial results**, does **dynamic linking**, receives **return values**, and is the context for **exception dispatch**. It is not the object, not the whole stack, and not the class — [[How would you explain the JVM stack and stack frames]], [[How would you explain the Java stack and heap]].

## One invocation, three pieces of storage

The Java Virtual Machine stack of a thread exists to **push and pop frames**. Invoke **creates** a frame from that thread’s JVM stack; the invocation’s completion — **normal or abrupt** — **destroys** it. Only the frame of the method actually running is **current**. Nested calls leave the caller’s frame waiting underneath.

That frame **represents**:

- **Local variables** — the method’s parameters and locally declared slots. Length is fixed at compile time. Instance methods put **`this` in local 0**; class methods start parameters at 0. `long` and `double` occupy **two** consecutive slots.
- **Operand stack** — working space for bytecode (empty at frame creation). It is LIFO; `long`/`double` count as two units of depth.
- **Dynamic linking** — a **reference** to the current class’s **run-time constant pool** (stored in the method area). Bytecodes name fields and methods symbolically; the frame is how this invocation resolves them.

On **normal** completion, a return instruction restores the caller and, if there is a result, **pushes it on the caller’s operand stack**. On **abrupt** completion (uncaught exception, including `athrow`), the invocation **returns no value**.

A frame created by a thread is **local to that thread** and cannot be referenced by another. Because the JVM stack is only used to push and pop frames, **frames may be heap-allocated** — the word “stack” does not mean a C array of the object’s fields.

```java
final class WhatAFrameIs {
    int scale;

    int times(int n) {
        int product = n * this.scale;
        return product;
    }

    public static void main(String[] args) {
        WhatAFrameIs o = new WhatAFrameIs();
        o.scale = 3;
        System.out.println(o.times(4));
    }
}
```

**Listing 1.** The `times` frame **is** that call: locals `this`, `n`, `product`, a short-lived operand stack for `imul`, and a link to `WhatAFrameIs`’s constant pool. The `WhatAFrameIs` instance stays on the heap after `times` returns and the frame is gone.

```d2
direction: down
inv: "invoke times" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
fr: "Frame = this invocation" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
  loc: "locals" { width: 90; height: 36 }
  op: "operand stack" { width: 120; height: 36 }
  cp: "link to constant pool" { width: 160; height: 36 }
}
done: "return or uncaught throw\nframe destroyed" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
inv -> fr
fr -> done
```

**Fig. 1.** A frame represents one activation. Destroying it does not free heap objects that locals still referred to from other frames.

> [!warning] A frame is not “the object on the stack”
> Locals hold **values** (including references). The instance those references denote is on the **heap**. After return, the frame is gone; reachability of the object is whatever other references remain.

> [!warning] Abrupt completion is still a frame, with no result
> An uncaught exception **destroys** the frame like a return does, but **no value** is passed to the caller. Exception dispatch uses the current frame’s context; it does not turn the frame into a heap object.

> [!tip] Interview answer
> A JVM stack frame is one method call on one thread: locals, operand stack, and a link to the class constant pool for linking. It is created on invoke and destroyed when that call completes, with a return value only on the normal path. The object lives on the heap; the frame is just that activation.
