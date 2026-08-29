<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS

# How would you explain `StackOverflowError` in Java?

> [!abstract] Short answer
> **It is an unchecked `Error` (`VirtualMachineError`) meaning this thread’s Java stack cannot hold another frame.** Deep or unbounded recursion is the usual cause. Filling the **heap** is `OutOfMemoryError`, not stack overflow. An infinite loop in one method does not push frames.

## One stack per thread, one frame per call

Each thread has a private Java Virtual Machine stack of **frames**. A new frame is created on method invocation (locals, operand stack, bookkeeping) and destroyed when that invocation completes. If the computation needs a **larger stack than is permitted**, the VM throws `StackOverflowError`. The API names the typical trigger: the application **recurses too deeply** ([[How do you produce a StackOverflowError]], [[What is VirtualMachineError]]).

It may also be thrown asynchronously from native-method execution or other VM stack limits. Native method stacks have the same “larger than permitted → `StackOverflowError`” rule.

That is not heap exhaustion. If there is not enough memory to **create or expand** a thread’s stack, the VM throws `OutOfMemoryError` instead ([[How would you explain OutOfMemoryError]]). `-Xss` (and the platform `Thread` stack-size constructor) change how much stack a thread is allowed; a larger stack can recurse deeper before overflow.

`StackOverflowError` extends `Error`, not `Exception`. `catch (Exception)` does not catch it. Catching it and continuing is not a repair ([[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]], [[Why should you not catch java.lang.Error]]).

```d2
direction: down
call: "method invoke" {
  width: 240
  height: 50
}
frame: "push frame on thread stack" {
  width: 280
  height: 50
}
limit: "stack still allowed?" {
  width: 260
  height: 50
}
ok: "run the method" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
soe: "StackOverflowError" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
call -> frame -> limit
limit -> ok: "yes"
limit -> soe: "no"
```

**Fig. 1.** Overflow is “this thread’s stack is full of frames,” not “the Java heap is full.”

```java
class Demo {
    static void blow() {
        blow();
    }
}
```

**Listing 1.** Each call adds a frame. There is no base case, so the thread hits the stack limit.

> [!warning] `while (true) {}` is not a `StackOverflowError`
> A tight loop in **one** frame never grows the stack. Unbounded **calls** do.

> [!warning] There is no `StackOverflowException`
> The type is `java.lang.StackOverflowError`. Treat it as a VM resource failure, not as a checked API signal.

> [!tip] Interview answer
> **`StackOverflowError` means this thread needed a deeper Java stack than the VM allows — almost always runaway recursion.** It is a `VirtualMachineError`, so `catch (Exception)` misses it. Heap pressure is `OutOfMemoryError`; a loop that never calls another method will not overflow the stack.
