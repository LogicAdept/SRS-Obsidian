<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# How do you produce a `StackOverflowError`?

> [!abstract] Short answer
> **Recurse without a terminating base case.** Each invocation pushes a frame on the thread’s Java Virtual Machine stack. When the computation needs a larger stack than is permitted, the VM throws `StackOverflowError`. Filling the heap with retained objects is `OutOfMemoryError`, not stack overflow.

## Unbounded recursion fills the Java stack

`StackOverflowError` extends `VirtualMachineError` (hence `Error`). The API states it is thrown when a stack overflow occurs because an application recurses too deeply ([[How would you explain StackOverflowError in Java]], [[What is VirtualMachineError]], [[What is java.lang.Error]]).

A new frame is created on each method invocation and destroyed when that invocation completes. Frames hold locals and the operand stack. Unbounded self-calls (or mutual recursion) never return, so frames accumulate until the thread’s stack cannot grow further.

```d2
direction: down
call: "m() calls m()" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
frames: "frames accumulate" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
soe: "StackOverflowError" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
loop: "while (true) {}" {
  width: 260
  height: 50
  style.fill: "#eceff1"
}
no: "no new frames" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
call -> frames -> soe
loop -> no
```

**Fig. 1.** Recursion consumes stack frames. A tight loop that never invokes a method does not.

```java
class Demo {
    static void recurse() {
        recurse();
    }

    static void recursivePrint(int n) {
        System.out.println(n);
        recursivePrint(n + 1);
    }

    static void spin() {
        while (true) { }
    }
}
```

**Listing 1.** `recurse` and `recursivePrint` produce `StackOverflowError`. `spin` does not: it never pushes another frame. There is no `StackOverflowException` type.

`Error` is unchecked. `catch (Exception e)` does not handle it ([[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]). Catching it is legal but usually wrong: the stack is already exhausted ([[Why should you not catch java.lang.Error]]).

> [!warning] Heap exhaustion is a different `Error`
> Allocating objects until the VM cannot make more memory available is `OutOfMemoryError`, not `StackOverflowError`. If the stack is allowed to expand and that expansion itself cannot obtain memory, the VM also throws `OutOfMemoryError` ([[How would you explain StackOverflowError OutOfMemoryError]], [[How do you reproduce an OutOfMemoryError in Java]]).

> [!warning] An infinite loop is not unbounded recursion
> `while (true) {}` burns CPU in one frame. It does not grow the Java stack the way `m()` calling `m()` does. Native-method stacks can overflow too, but the interview example is Java recursion.

> [!tip] Interview answer
> **Write a method that calls itself with no base case; each call adds a stack frame until the VM throws `StackOverflowError`.** It is an `Error`, not an `Exception`. A busy loop without calls stays in one frame; filling the heap is `OutOfMemoryError`.
