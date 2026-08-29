<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Error #SRS

# Does `catch (Exception)` also catch `Error`?

> [!abstract] Short answer
> **No.** `Error` is a sibling of `Exception` under `Throwable`, not a subclass. `catch (Exception e)` matches `IOException`, `RuntimeException`, `NullPointerException`, and other `Exception` subtypes. It does **not** match `OutOfMemoryError`, `StackOverflowError`, or any other `Error`. `catch (Throwable t)` matches both branches.

## The sibling split is the point of the tree

`Throwable` has two direct subclasses: `Exception` and `Error`. A `catch` handles a thrown object when the object's class is the catch type or a **subclass** of it. `Error` is not a subclass of `Exception`, so it is not assignment-compatible with `Exception`.

That layout exists so `catch (Exception e)` can take the throwables ordinary code might recover from, without also taking JVM-style failures on the `Error` branch. See [[Why is Error a sibling of Exception rather than a subclass]] and [[Do checked exceptions inherit Throwable directly]].

```d2
direction: down
throwable: "Throwable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
exc: "Exception\ncatch (Exception) hits here" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
err: "Error\nnot caught" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
rte: "RuntimeException\nalso caught" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
oom: "OutOfMemoryError\nnot caught" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
throwable -> exc
throwable -> err
exc -> rte
err -> oom
```

**Fig. 1.** `catch (Exception)` covers the left branch, including unchecked `RuntimeException`. It never walks into `Error`. Contrast [[Does catch Exception also catch RuntimeException]].

```java
class Demo {
    static void mayFail() {
        throw new OutOfMemoryError("demo");
    }

    static void catchException() {
        try {
            mayFail();
        } catch (Exception e) {
            // not reached: OutOfMemoryError is not an Exception
        }
    }

    static void catchThrowable() {
        try {
            mayFail();
        } catch (Throwable t) {
            // reached: Error is a Throwable
        }
    }
}
```

**Listing 1.** `catch (Exception)` misses `Error`. `catch (Throwable)` includes it. `catch (Error e)` is also legal.

`Error` and its subclasses are unchecked ([[Are Error subclasses checked or unchecked]]). That exemption is about `throws`, not about whether a `catch` may name them.

> [!warning] `Exception` is not a synonym for “anything throwable”
> Interview shorthand that “catch Exception catches everything” is false. It misses the entire `Error` tree. If you meant both branches, you must write `catch (Throwable)` — [[Can you catch Throwable]].

> [!warning] Sibling does not mean uncatchable
> You can still `catch (Error e)` or `catch (OutOfMemoryError e)`. The language allows it. Ordinary applications are not expected to recover from most `Error`s; that is advice, not a compile-time ban ([[Can you catch and handle java.lang.Error like normal exceptions]]).

> [!tip] Interview answer
> **No. `Error` is a sibling of `Exception` under `Throwable`, so `catch (Exception e)` never sees an `Error`. It does catch `RuntimeException` and other `Exception` subtypes. Use `catch (Throwable)` or `catch (Error)` if you intend to include that branch.**
