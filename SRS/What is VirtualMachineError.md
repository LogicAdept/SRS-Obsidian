<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# What is `VirtualMachineError`?

> [!abstract] Short answer
> **An abstract `Error` meaning the JVM is broken or has run out of resources it needs to keep going.** The interview children are `OutOfMemoryError` and `StackOverflowError`. It is unchecked; ordinary code should not catch it and “recover.”

## Resource / VM failure, not linkage

`VirtualMachineError` extends `Error`. You do not declare it in `throws`. `catch (Exception)` does not catch it ([[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]], [[Why should you not catch java.lang.Error]], [[What is the difference between RuntimeException and Error]]).

The JVM throws a `VirtualMachineError` subclass when an **internal error or resource limit** stops it from implementing the language: heap exhaustion, stack overflow, and similar. `OutOfMemoryError` and `StackOverflowError` are those children — they are **not** direct subclasses of `Error` sitting beside `VirtualMachineError` ([[How do you reproduce an OutOfMemoryError in Java]], [[How do you produce a StackOverflowError]], [[What is OutOfMemoryError Requested array size exceeds VM limit]]).

Loading, linking, and class initialization failures are **`LinkageError`** (`NoClassDefFoundError`, `ExceptionInInitializerError`, `NoSuchMethodError`). That is a different `Error` branch ([[What is LinkageError]]). `AssertionError` is also an `Error`, not a `VirtualMachineError` ([[Is AssertionError a subclass of Exception]]).

The class is **abstract**. You meet the concrete subtypes, not a `new VirtualMachineError()`.

```d2
direction: down
err: Error {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
vme: VirtualMachineError {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
le: LinkageError {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
oome: OutOfMemoryError {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
soe: StackOverflowError {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
ae: AssertionError {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
err -> vme
err -> le
err -> ae
vme -> oome
vme -> soe
```

**Fig. 1.** JVM resource failures hang under `VirtualMachineError`. Linkage and `assert` are other `Error` families.

```java
class Demo {
    static void recurse() {
        recurse();
    }

    static void catcher() {
        try {
            recurse();
        } catch (Exception e) {
            // does not run for StackOverflowError
        }
    }
}
```

**Listing 1.** Unbounded recursion throws `StackOverflowError` (`VirtualMachineError`). `catch (Exception)` misses it. Filling the heap is `OutOfMemoryError`, still under this parent — not a `RuntimeException`.

> [!warning] OOM and stack overflow are not siblings of `Error`
> They sit **under** `VirtualMachineError`. Whiteboard trees that hang `OutOfMemoryError` directly off `Error` skip a generation.

> [!warning] `NoClassDefFoundError` is not a `VirtualMachineError`
> Missing or broken class metadata is `LinkageError`. Heap/stack limits are `VirtualMachineError`. Mixing those catalogs is a common dump mix-up.

> [!tip] Interview answer
> **`VirtualMachineError` is an `Error` for a JVM that is broken or out of resources.** `OutOfMemoryError` and `StackOverflowError` are its children. It is unchecked and not for application recovery, and it is not the parent of linkage failures like `NoClassDefFoundError`.
