<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #Java/JVM/ClassLoaders #SRS

# How would you explain errors that surface at the JVM level?

> [!abstract] Short answer
> **They are `Error`s, not `Exception`s: the VM cannot implement the language, or cannot load/link/init a class.** Ordinary programs are not expected to recover. `catch (Exception e)` misses them. Not every throwable the JVM raises is an `Error` — divide-by-zero and NPE are `RuntimeException`s.

## Two `Error` families, plus language exceptions

When the VM **synchronously** detects an abnormal condition, JLS splits it three ways:

1. **Language violation** (expression does not have the usual meaning) — e.g. integer `/ 0` → `ArithmeticException`, bad array index. These are **`RuntimeException`**, not `Error`.
2. **Load, link, or initialize** — a **`LinkageError`** (`NoClassDefFoundError`, `NoSuchMethodError`, `UnsupportedClassVersionError`, `ExceptionInInitializerError`, …) ([[What is LinkageError]], [[What is the difference between ClassNotFoundException and NoClassDefFoundError]], [[What happens if you use a class after ExceptionInInitializerError]]).
3. **Internal failure or resource limit** — a **`VirtualMachineError`**: `OutOfMemoryError`, `StackOverflowError`, and rarer internals. These can also be **asynchronous** (not tied to one bytecode the way a `/` is) ([[What is VirtualMachineError]], [[How do you diagnose memory pressure and OutOfMemoryError]], [[How do you produce a StackOverflowError]]).

`Error` sits **beside** `Exception` so `catch (Exception e)` can mean “recoverable application failures” without taking VM collapse ([[What is java.lang.Error]], [[Why is Error a sibling of Exception rather than a subclass]], [[Are Error subclasses checked or unchecked]]). Errors are unchecked; you do not declare `throws OutOfMemoryError`. Catching them is legal and is not a recovery plan ([[Why should you not catch java.lang.Error]]).

`AssertionError` is an `Error` from a failed `assert`, not a heap/stack limit. Diagnose OOME from the **detail message** (heap vs Metaspace vs native), not from `catch`.

```d2
direction: down
th: "Throwable" {
  width: 200
  height: 40
}
ex: "Exception / RuntimeException\n(NPE, ArithmeticException)" {
  width: 300
  height: 70
}
err: "Error" {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
vme: "VirtualMachineError\n(OOME, SOE)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
link: "LinkageError\n(NCDFE, NSME)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
th -> ex
th -> err
err -> vme
err -> link
```

**Fig. 1.** JVM-level **errors** are the `Error` branch. Many JVM-detected bugs are still `RuntimeException`.

```java
class Demo {
    static int language(int n) {
        return n / 0; // ArithmeticException, not Error
    }

    static void heap() {
        java.util.List<byte[]> held = new java.util.ArrayList<>();
        for (;;) {
            held.add(new byte[1_000_000]);
        }
    }
}
```

**Listing 1.** `language` is a specified language exception. `heap` (under a small `-Xmx`) is a `VirtualMachineError`. `catch (Exception e)` catches the first and misses the second.

> [!warning] “The JVM threw it” ≠ `Error`
> Integer overflow does not throw. Integer `/ 0` throws `ArithmeticException`. NPE is `RuntimeException`. OOME/SOE/linkage failures are `Error`.

> [!warning] Do not treat OOME like `IOException`
> After heap or stack exhaustion the handler often cannot allocate. Leave `Error` to the uncaught handler unless you are shutting down.

> [!tip] Interview answer
> **JVM-level errors are `Error` subclasses: `VirtualMachineError` when the VM is out of heap or stack, `LinkageError` when a class cannot be loaded or linked.** They are unchecked and sit outside `Exception` on purpose. Language bugs like NPE are still `RuntimeException`, even though the VM throws them.
