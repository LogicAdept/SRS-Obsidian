<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Stack #OperatingSystems/MemoryHierarchy #SRS

# What is a stack overflow physically?

> [!abstract] Short answer
> On HotSpot it is the **thread’s native stack** running into **memory-protected guard pages** at the low end of that mapping (stacks grow **down**). The VM **bangs** (touches) pages ahead of the stack pointer so the OS **traps** before adjacent memory is used. A trap in the **yellow** zone becomes `StackOverflowError`; the **red** zone is **fatal**. The spec name for this is “the thread needs a larger Java Virtual Machine stack than is permitted” — [[How would you explain StackOverflowError in Java]], [[How would you explain the JVM stack and stack frames]].

## Mapped stack, then a trap, then `StackOverflowError`

Each Java thread has a contiguous **thread stack** in virtual memory, sized with `-Xss` (HotSpot rounds up to the **OS page** size; Linux/x64 default is 1024 KB). JVM **frames** (locals, operand stack) consume that space as calls nest. The API text says the error is thrown when an application **recurses too deeply**; physically any **deep call chain** or **large frames** that exhaust the mapping do the same.

HotSpot’s layout (low addresses at `stack_end()`):

- **Red zone** — deepest. Touching it is **unrecoverable**: the VM crashes and writes diagnostics.
- **Yellow zone** — **recoverable**. Create and throw `StackOverflowError`, **unprotect** yellow temporarily so handlers can run. If those handlers overflow too, they hit **red**.
- **Reserved zone** (optional) — extra room for methods marked `@ReservedStackAccess`; otherwise treated like yellow.
- **Shadow zone** — the band **ahead of SP** that code **bangs** so the trap happens in known VM/Java entry points, pages get **committed** on OSes with lazy stack growth, and the bang cannot skip into another thread’s stack.

The **entire guard zone is protected**, so a bang into it **traps**. That is the physical event: not a Java `if` on frame count, but a **fault on a guarded page**.

The JVMS also allows frames to be **heap-allocated**, and native methods use a **native method stack**. HotSpot’s overflow check is this **thread-stack** machinery, not “the heap filled with frames.” Exhausting the **object heap** is `OutOfMemoryError`, a different area — [[How would you explain OutOfMemoryError]].

```java
final class DeepRecursion {
    static void go(int n) {
        go(n + 1);
    }

    public static void main(String[] args) {
        go(0);
    }
}
```

**Listing 1.** Conceptual: each `go` call pushes another frame toward the guard pages. `-Xss` changes how soon the yellow-zone trap fires. Do not run this expecting a clean shutdown if handlers then hit red.

```d2
direction: down
high: "stack_base()  (high addresses)\nframe 0 … frame n" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
shadow: "shadow zone: bang ahead of SP" {
  width: 300
  height: 40
  style.fill: "#fff8e1"
}
guard: "reserved / yellow / red\n(protected pages)" {
  width: 300
  height: 55
  style.fill: "#ffebee"
}
end: "stack_end()  (low addresses)" {
  width: 300
  height: 40
}
high -> shadow
shadow -> guard: "SP grows down"
guard -> end
```

**Fig. 1.** HotSpot thread stack grows toward protected guard pages. Yellow trap → `StackOverflowError`; red trap → VM abort.

> [!warning] Catching `StackOverflowError` still needs stack
> Yellow protection is **removed** so handlers can run. If the handler, logging, or another call **bangs red**, the process **dies**. This is still a `VirtualMachineError`; do not treat it as a normal control-flow exception.

> [!warning] This is not heap exhaustion
> `-Xmx` does not size the thread stack. Growing `-Xmx` will not stop a yellow-zone overflow. Failing to **create** a thread stack at all is `OutOfMemoryError`, not `StackOverflowError`.

> [!tip] Interview answer
> Physically the thread has a fixed mapped stack (`-Xss`) that grows downward into protected guard pages. HotSpot bangs pages ahead of the stack pointer; a yellow-zone fault becomes `StackOverflowError`, a red-zone fault kills the VM. Deep recursion is the usual way to get there, but it is stack **space**, not a Java-level recursion counter.
