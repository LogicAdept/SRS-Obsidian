<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What is `NullPointerException`?

> [!abstract] Short answer
> **An unchecked `RuntimeException` when code uses `null` where an object is required.** Typical cases: an instance method or field on a null reference, `length` or an index on a null array, unboxing a null wrapper, or `throw null`.

## `null` used as an object

`NullPointerException` extends `RuntimeException`. You do not declare it in `throws`. The JVM may construct it with suppression disabled and a non-writable stack ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]]).

It is thrown when an instance method runs on a null target, a field (including an array’s `length`) is read or written through null, a null reference is indexed as an array, a wrapper is unboxed, or `throw` evaluates to `null` (the VM throws NPE instead of `null`). `synchronized (null)` also throws it.

A newly created `String[4]` has four **null slots**. `a[0].isEmpty()` NPEs. `a[4]` on a non-null array is `ArrayIndexOutOfBoundsException`. Indexing a **null** array is NPE, not that bounds type ([[What is ArrayIndexOutOfBoundsException]], [[How do you avoid NullPointerException when unboxing a Map value]]).

Empty `Optional.get()` is `NoSuchElementException`, not NPE ([[What is NoSuchElementException]], [[How do you prevent a NullPointerException]]).

`Objects.requireNonNull` throws this type on purpose for a forbidden null argument ([[What does Objects.requireNonNull do]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]]). JVM-thrown NPEs can include a helpful `getMessage()` ([[What did Java 14 change about NullPointerException messages]]).

```d2
direction: down
use: "null used as an object" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
npe: "NullPointerException" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
get: "Optional.empty().get()" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
nsee: "NoSuchElementException" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
use -> npe
get -> nsee
```

**Fig. 1.** Null-as-object versus empty `Optional.get()`.

```java
class Demo {
    static int methodOnNull() {
        String s = null;
        return s.length();
    }

    static int unbox() {
        Integer n = null;
        return n;
    }

    static void throwNull() {
        throw null;
    }

    static int slotThenDeref() {
        String[] a = new String[4];
        return a[0].length();
    }
}
```

**Listing 1.** All four methods throw `NullPointerException` at run time. `slotThenDeref` fails on the **element**, not because the array is missing. You may catch NPE like any unchecked exception ([[Can you catch an unchecked exception in Java]]). None of these needs `throws`.

> [!warning] Empty `Optional.get()` is not NPE
> `Optional` is present or absent. Empty `get()` throws `NoSuchElementException`. Catching NPE around `get()` is the wrong type.

> [!warning] Null array vs null **slot** vs bad index
> `String[] a = null; a[0]` is NPE. `new String[4]; a[0].length()` is NPE on the slot. `a[4]` on that array is `ArrayIndexOutOfBoundsException`.

> [!warning] Static access through a null qualifier need not NPE
> `nullRef.staticMethod()` can still run the static method. NPE is for **instance** use of null. Interview snippets that “always NPE on a dot” miss that case.

> [!tip] Interview answer
> **`NullPointerException` is an unchecked `RuntimeException` when you use `null` as an object** — method or field, null array, unbox, or `throw null`. Empty `Optional.get()` is `NoSuchElementException`, and a missing array index on a real array is `ArrayIndexOutOfBoundsException`, not NPE.
