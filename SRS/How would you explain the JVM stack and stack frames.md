<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Stack #SRS

# How would you explain the JVM stack and stack frames?

> [!abstract] Short answer
> Each Java thread has a private **Java Virtual Machine stack**, created with the thread. The stack exists only to **push and pop frames**. A **frame** is the activation of one method: **local variables**, an **operand stack**, and a **reference** to that class’s run-time constant pool. Invoke creates a frame; return or an uncaught throw **destroys** it. The heap still holds the objects; the frame holds **values**, including references — [[How would you explain the Java stack and heap]], [[What JVM runtime memory regions exist]].

## One stack per thread, one current frame

The JVM stack is analogous to a conventional call stack, but you never index it as an array: the only operations are pushing and popping frames. Memory for the stack need not be contiguous. Because of that restriction, **frames may be heap-allocated**. Size is typically `-Xss` (HotSpot rounds up to a page; the default is platform-specific, for example 1024 KB on Linux/x64). Too much depth → `StackOverflowError`. Failing to create or expand a stack → `OutOfMemoryError` — [[How would you explain StackOverflowError in Java]].

A frame is created on every method invocation and destroyed when that invocation completes, **normally or abruptly**. Only one frame is **current** in a thread: the running method. Call another method and a new frame becomes current; return and the previous frame is current again, with any return value pushed on **its** operand stack.

Each frame contains:

- **Local variables** — length fixed at compile time. One slot for `int` / `reference` / …; **two consecutive slots** for `long` and `double`. On an **instance** method, **local 0 is `this`**; parameters start at 1. On a **class** method, parameters start at 0.
- **Operand stack** — empty when the frame is created; bytecodes push and pop working values. `long`/`double` count as **two** units of depth. Max depth is compile-time.
- **Dynamic linking** — a reference to the class’s **run-time constant pool** (in the method area, not copied into the frame) so symbolic field/method refs can be resolved.

The per-thread **`pc`** names the current bytecode when the current method is not `native`. While a `native` method runs, `pc` is undefined; that work uses the optional **native method stack**, not a JVM frame of Java locals.

```java
final class FrameLocals {
    int field;

    int add(int a, int b) {
        int sum = a + b;
        return sum + this.field;
    }

    public static void main(String[] args) {
        System.out.println(new FrameLocals().add(1, 2));
    }
}
```

**Listing 1.** In `add`, local 0 is `this`, then `a`, `b`, and `sum`. `iadd` uses the operand stack. The `FrameLocals` instance and `field` are on the heap. `main` is a class method: its `args` reference starts at local 0.

```d2
direction: down
th: "Java thread" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
st: "JVM stack" {
  width: 280
  height: 40
}
f2: "current frame: add\nlocals this,a,b,sum\noperand stack" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
f1: "caller frame: main\nlocals args\nwaits for return" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
th -> st
st -> f2
st -> f1
```

**Fig. 1.** Nested frames on one thread’s JVM stack. Only the top frame is current. Completing `add` discards its frame and pushes the `int` result onto `main`’s operand stack.

> [!warning] The JVM stack is not the native C stack
> Frames may be **heap-allocated**. `-Xss` sizes the **thread** stack HotSpot uses; `native` methods use a **separate** native stack when the VM provides one. Overflow of Java frames is `StackOverflowError`, not a heap `OutOfMemoryError`.

> [!warning] Local 0 is `this` only on instance methods
> `static` methods pack parameters from slot 0. `long`/`double` still take two slots, so later indexes skip. The operand stack is **not** the local-variable array; mixing them is a verifier error.

> [!tip] Interview answer
> Each thread has a JVM stack of frames. A frame is one call: locals, operand stack, and a link to the class constant pool. Instance methods put `this` in local 0. The frame dies when the method returns or throws out; objects those locals referred to stay on the shared heap until they are unreachable.
