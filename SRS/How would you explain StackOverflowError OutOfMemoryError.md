<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS

# How would you explain `StackOverflowError` `OutOfMemoryError`?

> [!abstract] Short answer
> **Both are unchecked `VirtualMachineError`s, but they name different resources.** `StackOverflowError` means **this thread’s Java stack cannot hold another frame** (deep or unbounded recursion). `OutOfMemoryError` means an **allocation failed** — usually the Java heap, but also Metaspace, GC-overhead policy, native threads, or an oversize array. `catch (Exception)` misses both.

## Stack frames versus heap (and other) pools

A thread’s JVM stack holds **frames**: one per live method invocation. If the computation needs a larger stack than is permitted, the VM throws `StackOverflowError`. Typical cause: recursion with no base case, or a call chain that is simply too deep. A `while (true)` loop in **one** method does not push frames ([[How would you explain StackOverflowError in Java]], [[How do you produce a StackOverflowError]]).

`OutOfMemoryError` is thrown when the VM cannot satisfy an allocation (object, metadata, or some native resource) and the collector cannot make enough room. The **detail message** names the pool: `Java heap space`, `GC overhead limit exceeded`, `Metaspace`, native thread creation, `Requested array size exceeds VM limit`, and related native/swap text ([[How would you explain OutOfMemoryError]], [[How do you reproduce an OutOfMemoryError in Java]]).

If there is not enough memory to **create or expand** a thread stack, that failure is `OutOfMemoryError`, not `StackOverflowError`. Overflow of an **existing** stack is `StackOverflowError`. `-Xss` sizes the stack; `-Xmx` sizes the heap. Raising one does not fix the other.

Both extend `Error`. Do not treat them as recoverable application exceptions ([[What is VirtualMachineError]], [[Does catch Exception also catch Error]], [[Why should you not catch java.lang.Error]]).

```d2
direction: right
soe: "StackOverflowError\nthis thread's frames" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
oom: "OutOfMemoryError\nheap / Metaspace / native" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Same `Error` family; stack depth versus an allocation that will not fit.

```java
class Demo {
    static void recurse() {
        recurse();
    }

    static void retain() {
        java.util.List<byte[]> hold = new java.util.ArrayList<>();
        while (true) {
            hold.add(new byte[1_000_000]);
        }
    }
}
```

**Listing 1.** `recurse()` grows the **stack**. `retain()` grows reachable **heap** objects.

> [!warning] Default stack size is not a spec number
> `-Xss` defaults **depend on the platform**. Memorizing “512 KB” or “1 MB” is not the distinction.

> [!warning] `OutOfMemoryError` is not only the heap
> Metaspace, GC-overhead, native threads, and oversize arrays use the same type with **different** messages. `-Xmx` does not size those pools.

> [!tip] Interview answer
> **`StackOverflowError` is this thread running out of stack frames — usually runaway recursion.** **`OutOfMemoryError` is a failed allocation**, most often the heap, but the detail string tells you which pool. They are both `VirtualMachineError`s; `catch (Exception)` sees neither.
