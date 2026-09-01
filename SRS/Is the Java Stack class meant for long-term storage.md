<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/ArrayDeque #Java/JVM/Memory #SRS

> [!abstract] Short answer
> **No.** `java.util.Stack` is a LIFO API on a `Vector` — `push` / `pop` / `peek` — not a general warehouse and not the JVM’s per-thread stack. A `Stack` instance is a heap object, so elements stay reachable until you remove them or drop the collection. That lifetime is ordinary collection reachability, not “this class is for long-term storage.”

## Two different “stacks”

Interview wording “long-term storage” usually mixes **`java.util.Stack`** with the **Java Virtual Machine stack**. They share a name and LIFO shape. They are not the same thing ([[How would you explain the two main JVM memory regions stack and heap]]).

Each thread has a private JVM stack that stores **frames**. A frame is created when a method is invoked and **destroyed when that invocation completes** (normal return or uncaught exception). That structure holds locals and partial results for the call; it is not a place you park application entities for the life of the process. (Implementations may even heap-allocate frames; the spec point is lifetime, not a RAM cartoon.)

`java.util.Stack` is a class instance. Class instances and arrays are allocated from the **heap**. The five stack methods sit on a growable `Vector`: `push` is `addElement` at the last index ([[How would you explain Stack how why]]). Nothing in that API expires an element. If you leave a `Stack` in a field, everything still in it stays reachable — same as `ArrayList` or `ArrayDeque`.

```d2
direction: right
jvm: "JVM stack (per thread)\nframes: invoke → complete" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
cls: "java.util.Stack\nheap Collection, LIFO methods" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
use: "Want LIFO in code?\nDeque + ArrayDeque" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
cls -> use: "prefer"
```

**Fig. 1.** Frame lifetime vs a heap `Vector` with stack methods. Do not answer “the stack is temporary” if the question named the **class**.

Because `Stack` is-a `List`, you *can* treat it as indexed storage for as long as you like. That is the leak, not the purpose. The documented job is LIFO; the documented replacement is `Deque`, usually `ArrayDeque` ([[How do you use a Deque as a stack]], [[Why is java.util.Stack discouraged and what should you use instead]]). A long-lived **list** is `ArrayList` (or `Vector` only if you still want its synchronization) — not `Stack` as a warehouse ([[Why was ArrayList added when Vector already existed]]).

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Stack;

class StackLifetime {
    static final Stack<String> field = new Stack<>();

    static void demo() {
        field.push("survives demo() return"); // heap Collection, still reachable
        String top = field.peek();

        Deque<String> stack = new ArrayDeque<>();
        stack.push("LIFO without Vector");
        stack.pop();
    }
}
```

**Listing 1.** `field` keeps the string after `demo` returns — collection reachability, not a JVM frame. New LIFO code still uses `ArrayDeque`.

> [!warning] “Temporary” is the JVM stack, not `java.util.Stack`
> Method frames vanish when the call completes. `Stack.push` does not. Saying the **class** is “only short-term storage” is false: there is no TTL. Saying it is a good long-lived `List` is also false: that is `Vector` leaking through.

> [!warning] Prefer `Deque` even when the `Stack` lives for hours
> A long-lived LIFO field should still be `Deque` / `ArrayDeque`. Longevity does not make `java.util.Stack` the right type: you still inherit `List`, locks, and `EmptyStackException`.

> [!tip] Interview answer
> **No — `java.util.Stack` is a LIFO `Vector`, not long-term storage and not the JVM stack.** Frames are created on invoke and destroyed when the method completes; a `Stack` object lives on the heap and keeps references until you pop or drop it. For LIFO in application code use `ArrayDeque`; for a list use `ArrayList`.
