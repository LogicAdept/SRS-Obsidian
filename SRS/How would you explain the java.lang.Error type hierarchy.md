<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Exceptions/Hierarchy #SRS

# How would you explain the `java.lang.Error` type hierarchy?

> [!abstract] Short answer
> **`Error` is a direct subclass of `Throwable`, a sibling of `Exception`.** Every `Error` is **unchecked**. Interview the tree as three forks: **`VirtualMachineError`** (resources / VM internals), **`LinkageError`** (load, link, init), and **other `Error`s** such as `AssertionError`. `catch (Exception)` matches none of them.

## Sibling of `Exception`, not a kind of it

`Error` exists so ordinary recovery can use `catch (Exception)` without catching conditions a reasonable application should not try to catch ([[What is java.lang.Error]], [[Why is Error a sibling of Exception rather than a subclass]], [[Does catch Exception also catch Error]], [[Are Error subclasses checked or unchecked]]). You may still write `catch (Error)`, but that is not recovery ([[Why should you not catch java.lang.Error]]).

**`VirtualMachineError`** is the resource / internals fork: `OutOfMemoryError`, `StackOverflowError`, and related types. These are not siblings of `Error`; they sit **under** it ([[What is VirtualMachineError]], [[How would you explain OutOfMemoryError]], [[How would you explain StackOverflowError in Java]], [[How would you explain errors that surface at the JVM level]]).

**`LinkageError`** is the class-loading / binary-compatibility fork: a class cannot be linked or has become incompatible. Children include `NoClassDefFoundError` and `ExceptionInInitializerError`. That is not `ClassNotFoundException` (checked, under `Exception`) ([[What is LinkageError]], [[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

**Direct `Error`s that are neither VME nor linkage** include `AssertionError` (`assert` failed) and `IOError`. `ThreadDeath` is still an `Error`, but it is deprecated for removal; `Thread.stop` is gone ([[Is AssertionError a subclass of Exception]], [[What is ThreadDeath]], [[How would you explain the Java exception type hierarchy]]).

```d2
direction: down
err: "Error" {
  width: 220
  height: 50
}
vme: "VirtualMachineError" {
  width: 280
  height: 50
}
link: "LinkageError" {
  width: 260
  height: 50
}
other: "AssertionError / IOError" {
  width: 280
  height: 50
}
oom: "OutOfMemoryError" {
  width: 260
  height: 50
}
soe: "StackOverflowError" {
  width: 260
  height: 50
}
ncd: "NoClassDefFoundError" {
  width: 280
  height: 50
}
err -> vme
err -> link
err -> other
vme -> oom
vme -> soe
link -> ncd
```

**Fig. 1.** `Error` is the branch. `OutOfMemoryError` is not a sibling of `Error`.

```java
class Demo {
    static void kinds(Error e) {
        System.out.println(e instanceof Exception);
        System.out.println(e instanceof VirtualMachineError);
        System.out.println(e instanceof LinkageError);
    }
}
```

**Listing 1.** Every `Error` prints `false` for `Exception`. An `OutOfMemoryError` is a `VirtualMachineError`; a `NoClassDefFoundError` is a `LinkageError`.

> [!warning] `Error` is not “the JVM-only folder”
> `AssertionError` is an `Error` and is **not** a `VirtualMachineError`. Linkage failures are `Error`s too.

> [!warning] Name collisions with `Exception`
> `NoSuchMethodError` is not `NoSuchMethodException`. `NoClassDefFoundError` is not `ClassNotFoundException`. The suffix is the hierarchy.

> [!tip] Interview answer
> **`Error` sits beside `Exception` under `Throwable`; all of it is unchecked.** Draw three forks: VM resources (`VirtualMachineError`), linkage (`LinkageError`), and the rest (`AssertionError`). `catch (Exception)` never sees this branch, and catching `Error` is not a recovery strategy.
