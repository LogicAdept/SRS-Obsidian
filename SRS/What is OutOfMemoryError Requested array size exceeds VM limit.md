<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS

# What is `OutOfMemoryError: Requested array size exceeds VM limit`?

> [!abstract] Short answer
> **An `OutOfMemoryError` detail message when the program asks for an array longer than this VM will allocate — even if the heap still has free space.** Raising `-Xmx` does not fix it. It is a different flavor from `Java heap space` and from `GC overhead limit exceeded`.

## VM max length, not “heap is a bit small”

`OutOfMemoryError` is an unchecked `Error` (`VirtualMachineError`). `catch (Exception)` does not catch it ([[What is java.lang.Error]], [[What is VirtualMachineError]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]).

The JVM appends a **detail message** so you can tell *why* allocation failed. `Requested array size exceeds VM limit` means the requested **length** is past the implementation’s maximum array size, **irrespective of how much heap is available**. The fix is a smaller length (or a bug that computed a huge size), not a bigger heap.

`Java heap space` is the opposite story: the object (including a large-but-legal array) could not be placed in the Java heap. There `-Xmx` / `-Xms` matter. `GC overhead limit exceeded` means the collector is running almost constantly and reclaiming almost nothing ([[How do you reproduce an OutOfMemoryError in Java]], [[How do you diagnose memory pressure and OutOfMemoryError]], [[How would you explain OutOfMemoryError]]).

A negative dimension is `NegativeArraySizeException`, not this message. A huge **legal** length such as `new Integer[1_000_000_000]` under a tiny `-Xmx` is usually **`Java heap space`**, which is what dump snippets that mix this message with a billion-slot array often get wrong.

```d2
direction: down
oome: "OutOfMemoryError" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}
vm: "Requested array size exceeds VM limit" {
  width: 360
  height: 50
  style.fill: "#ffebee"
}
heap: "Java heap space" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
gc: "GC overhead limit exceeded" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
oome -> vm
oome -> heap
oome -> gc
```

**Fig. 1.** Same `Error` type; the detail message is the diagnosis.

```java
class Demo {
    static Integer[] billionSlots() {
        return new Integer[1_000_000_000];
    }
}
```

**Listing 1.** `billionSlots` is a legal `int` length. With a small `-Xmx` it typically fails as **`Java heap space`**. The **VM limit** message is a length this JVM will not allocate at all, even with a large heap. Stack overflow is a different `Error` ([[How do you produce a StackOverflowError]]).

> [!warning] `-Xmx` does not raise the max array length
> This message is independent of free heap. If dumps say “array bigger than the heap,” they are describing an older or looser wording. The current distinction is: length past the **VM implementation limit**.

> [!warning] A billion slots is not automatically this message
> `new Integer[1000 * 1000 * 1000]` is a common dump example under tiny `-Xmx`. That size is usually heap exhaustion (`Java heap space`), not “exceeds VM limit.”

> [!tip] Interview answer
> **`OutOfMemoryError: Requested array size exceeds VM limit` means the array length is past what this VM will allocate, even if the heap is not full.** Do not confuse it with `Java heap space` (raise `-Xmx`) or `GC overhead limit exceeded`. A negative size is `NegativeArraySizeException`.
