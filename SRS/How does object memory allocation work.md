<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #DataAndState/MemoryManagement #SRS

# How does object memory allocation work?

> [!abstract] Short answer
> A class instance or array is an **object**. Memory for it comes from the **heap**, which is shared by every Java thread. `new` first **reserves** that space (or throws `OutOfMemoryError`), **default-initializes** every instance field including hidden superclass fields, then runs constructors. The local variable or operand-stack slot holds a **reference** (a pointer), not the object — [[Is it true that primitives live on the stack and reference instances live on the heap]], [[Can primitive values reside on the Java heap]].

## Heap first, then constructors

The heap is created at VM start-up. Class instances and arrays are allocated from it. There is no explicit free; a garbage collector reclaims storage. If the collector cannot make enough heap available, the VM throws `OutOfMemoryError` — [[How would you explain OutOfMemoryError]]. The VM does **not** mandate an object layout; HotSpot’s headers and field packing are an implementation, not a language rule.

For `new C(args)` the run-time order is:

1. Allocate space for every instance variable of `C` and its superclasses (including hidden fields).
2. If that fails, throw `OutOfMemoryError` **before** evaluating `args`.
3. Set every new field to its default (`0` / `0.0` / `false` / `null`).
4. Evaluate constructor arguments left to right, then run the constructor chain (`super` / `this`, then instance initializers, then the constructor body).

Array creation is the other way around: dimension expressions run **first**, then the heap allocation. The `new` bytecode only makes an **uninitialized** instance; creation is unfinished until an instance initializer (`<init>`) has run.

HotSpot’s fast path (default **`-XX:+UseTLAB`**) gives each mutator thread a **thread-local allocation buffer** in young / Eden space. Allocation is a pointer bump: if `end - top` is large enough, `top` advances and the object sits in that buffer. Those objects are still ordinary heap objects; other threads can reach them. If the buffer is short, HotSpot refills a TLAB or allocates **outside** it in shared space (that path can trigger GC). On G1, an object at least **half a heap region** is **humongous**: it is allocated as contiguous **old** regions, not into Eden.

Class variables are **not** in the instance. They are created when the class is prepared and live with the class, not with each `new`.

```java
class Super {
    Super() {
        show();
    }

    void show() {}
}

class Sub extends Super {
    int n = 7;

    @Override
    void show() {
        System.out.println(n);
    }

    public static void main(String[] args) {
        new Sub();
    }
}
```

**Listing 1.** Prints `0`, not `7`. The object is already on the heap with default field values while `Super`’s constructor runs. `n = 7` is an instance initializer and runs only after `super()` returns.

```d2
direction: down
expr: "new C(args)" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
alloc: "Reserve heap words\n(TLAB bump or shared)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
oom: "OutOfMemoryError\nargs not evaluated" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}
zero: "Default-init all instance fields" {
  width: 280
  height: 45
  style.fill: "#fff8e1"
}
ctor: "Eval args, then <init> chain" {
  width: 280
  height: 45
  style.fill: "#f3e5f5"
}
ref: "Push reference; object stays on heap" {
  width: 300
  height: 45
}
expr -> alloc
alloc -> oom: "not enough heap"
alloc -> zero: "space obtained"
zero -> ctor
ctor -> ref
```

**Fig. 1.** Language order for class instance creation. HotSpot’s TLAB is only the usual way to obtain the heap words in step one.

> [!warning] `new C(expr)` can throw before `expr` runs
> Heap exhaustion is detected **before** constructor arguments. A side-effecting argument does not run if allocation fails. `new T[n]` is the opposite: `n` is evaluated first, then the array is allocated.

> [!warning] A TLAB is not a private object
> The buffer is per-thread so allocation needs no shared-heap CAS on the fast path. The object is still on the shared heap. Publishing `this` from a constructor, or calling an override from `super()`, exposes a heap object whose subclass fields may still be defaults.

> [!tip] Interview answer
> Objects live on the shared heap; `new` reserves that memory, zeros instance fields, then runs constructors, and the stack only holds the reference. If the heap cannot satisfy the request you get `OutOfMemoryError` before constructor arguments run. HotSpot usually bump-allocates in a per-thread TLAB in Eden; a too-large G1 object bypasses Eden and is allocated as humongous old regions.
