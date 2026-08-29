<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# What sits at the root of every Java exception?

> [!abstract] Short answer
> **`java.lang.Throwable`.** Every thrown object is a `Throwable` (or `throw null`, which becomes `NullPointerException`). `Exception` and `Error` are the two direct subclasses. `Object` is the root of all classes, not of the exception types you `throw`.

## `Throwable`, then two branches

The language’s exception classes are `Throwable` and its subclasses. Only types assignable to `Throwable` may appear in `throw` or `catch` ([[Can you throw an object that is not a Throwable]], [[How would you explain exception]], [[How would you explain the Java exception type hierarchy]]).

`Exception` is the recover-from branch; `Error` is the not-ordinarily-recoverable sibling. Checked types are `Throwable` minus `RuntimeException` and minus `Error`, so **`Throwable` itself is checked** ([[Is Throwable a checked exception]], [[Do checked exceptions inherit Throwable directly]], [[Why is Error a sibling of Exception rather than a subclass]]).

A custom class that extends `Throwable` directly is checked and is **not** caught by `catch (Exception)`.

```d2
direction: down
obj: "Object" {
  width: 220
  height: 50
}
th: "Throwable" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
ex: "Exception" {
  width: 240
  height: 50
}
err: "Error" {
  width: 240
  height: 50
}
obj -> th
th -> ex
th -> err
```

**Fig. 1.** The exception root is `Throwable`, not `Object` and not `Exception`.

```java
class Demo {
    static void show(Throwable t) {
        System.out.println(t instanceof Throwable);
        System.out.println(t instanceof Exception);
        System.out.println(t instanceof Error);
    }
}
```

**Listing 1.** Every catchable/thrown object is a `Throwable`. Only some are `Exception`; `Error` is the other branch.

> [!warning] The root is not `Exception`
> Saying “everything extends `Exception`” drops `Error` and a direct `Throwable` subclass.

> [!warning] `throw null` is not a non-`Throwable`
> It is evaluated, then a `NullPointerException` is thrown.

> [!tip] Interview answer
> **`Throwable` is the root of every Java exception type.** `Exception` and `Error` sit under it as siblings. You can only `throw` a `Throwable` (or `null`, which becomes `NullPointerException`).
