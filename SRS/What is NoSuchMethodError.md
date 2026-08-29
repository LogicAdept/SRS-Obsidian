<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# What is `NoSuchMethodError`?

> [!abstract] Short answer
> **An unchecked `Error` when code calls a method the runtime class no longer defines.** The compiler would have rejected a missing method; this type appears at run time after an incompatible class change — partial rebuild or a library version that dropped or changed the signature. It is **not** `NoSuchMethodException`.

## Binary mismatch, not reflective lookup

`NoSuchMethodError` extends `IncompatibleClassChangeError`, hence `LinkageError` and `Error`. You do not declare it in `throws`. `catch (Exception)` does not catch it ([[What is LinkageError]], [[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]).

The JVM throws it while resolving a symbolic method reference: the caller was compiled against a method (static or instance) that the loaded class no longer has. Deleting a method, or changing its signature so the old descriptor is gone, is the usual production case.

`Class.getMethod` / `getDeclaredMethod` when the name or parameter types are wrong throw the **checked** `NoSuchMethodException` (`ReflectiveOperationException`). That is a look-up miss in this process, not a stale `.class` file ([[What are common examples of checked exceptions in Java]]).

Dumps that show `Exception in thread "main" java.lang.NoSuchMethodError: main` are treating a missing launch `main` as this type. The language does not define that launch failure as `NoSuchMethodError`. The definition is a **call site** whose method vanished from the runtime type.

```d2
direction: down
err: Error {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
le: LinkageError {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
icce: IncompatibleClassChangeError {
  width: 280
  height: 40
  style.fill: "#ffebee"
}
nsme: NoSuchMethodError {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
ex: Exception {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
roe: ReflectiveOperationException {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
nsx: NoSuchMethodException {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
err -> le
le -> icce
icce -> nsme
ex -> roe
roe -> nsx
```

**Fig. 1.** `NoSuchMethodError` is an `Error`. Reflective “no such method” is a checked `Exception`.

```java
class Demo {
    static java.lang.reflect.Method lookup() throws NoSuchMethodException {
        return String.class.getDeclaredMethod("noSuchMethodHere");
    }
}
```

**Listing 1.** `lookup` throws **`NoSuchMethodException`** (checked) because reflection cannot find that method. A `NoSuchMethodError` needs two binaries: a caller compiled against `Helper.foo()` and a `Helper` at run time that no longer declares `foo`.

> [!warning] `Error` versus `Exception` — one letter, two hierarchies
> `NoSuchMethodError` is linkage. `NoSuchMethodException` is reflection and is checked. Mixing them is the standard name trap, same family as `ClassNotFoundException` vs `NoClassDefFoundError` ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

> [!warning] Missing `main` is not the definition
> Interview snippets that launch a class with no `main` are a launcher story, not the binary-compatibility type. Production `NoSuchMethodError` is “we compiled against library 2.x and ran 3.x” (or a half-rebuilt tree).

> [!tip] Interview answer
> **`NoSuchMethodError` is an unchecked `Error` when a method the compiler saw is gone from the class at run time.** Think jar version skew or a partial rebuild. Reflection’s miss is `NoSuchMethodException`, a checked exception, not this type.
