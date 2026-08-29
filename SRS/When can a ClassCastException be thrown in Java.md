<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# When can a `ClassCastException` be thrown in Java?

> [!abstract] Short answer
> **When a reference cast is not allowed at run time: the object’s class is not compatible with the target type.** That includes a written `(T) expr` and **hidden casts** the compiler inserts for generics. It is an unchecked `RuntimeException`. Casting `null` to a reference type does **not** throw.

## Failed cast, including ones you did not write

A cast expression converts or checks a value. Some casts are proven safe at compile time (for example to a superclass). Others need a run-time check. If that check fails, the VM throws `ClassCastException` ([[What is RuntimeException]], [[What are common kinds of unchecked exceptions in Java]], [[How would you explain exception]]).

The same exception is used for **automatically generated** casts that protect operations on non-reifiable generic types after an unchecked warning (heap pollution). Bridge methods / erasure can throw it **before** a method body runs if an argument is not an instance of the erased parameter type.

`instanceof` answers “could this be cast without `ClassCastException`?” without throwing (and is `false` for `null`). A `null` reference may be cast to any reference type.

Storing into an array whose run-time component type does not accept the value is **`ArrayStoreException`**, not `ClassCastException`. `Comparable`/`Comparator` may throw `ClassCastException` when elements are not mutually comparable.

```d2
direction: down
cast: "(T) expr" {
  width: 260
  height: 50
}
ok: "run-time type OK for T?" {
  width: 280
  height: 50
}
val: "value of type T" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
cce: "ClassCastException" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
cast -> ok
ok -> val: "yes"
ok -> cce: "no"
```

**Fig. 1.** A failed reference cast is `ClassCastException`. `null` takes the success path.

```java
class Demo {
    static Integer bad() {
        Object o = "x";
        return (Integer) o;
    }
}
```

**Listing 1.** `String` is not an `Integer`. The cast throws `ClassCastException`. `(Integer) null` does not.

> [!warning] `instanceof` does not throw `ClassCastException`
> Use it (or `Class.isInstance`) to test. The cast is what throws.

> [!warning] Heap pollution looks like a “random” CCE
> After an unchecked conversion, a later implicit cast can fail far from the raw `List` write. That is still a failed cast, not a different type.

> [!tip] Interview answer
> **`ClassCastException` is thrown when a reference cast is illegal at run time.** The usual demo is `(Integer) anObjectThatIsAString`. `null` does not throw, `instanceof` does not throw, and a bad array store is `ArrayStoreException`.
