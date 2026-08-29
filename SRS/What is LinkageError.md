<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# What is `LinkageError`?

> [!abstract] Short answer
> **An unchecked `Error` for a class that depends on another type that is missing or incompatibly changed at run time.** Subclasses include `NoClassDefFoundError`, `ExceptionInInitializerError`, and resolution failures such as `NoSuchMethodError`. It is not `ClassNotFoundException`.

## Load, link, initialize — not reflective “name not found”

`LinkageError` extends `Error`. You do not declare it in `throws`. `catch (Exception)` does not catch it ([[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]).

The JVM throws a `LinkageError` subclass when loading, linking, or initializing a class fails. Loading: no binary (`NoClassDefFoundError`), bad class file, circular hierarchy. Linking: verification (`VerifyError`) or resolving a symbolic reference (`NoSuchMethodError`, `NoSuchFieldError`, `IllegalAccessError`). A `native` method with no implementation is `UnsatisfiedLinkError` ([[What is NoSuchMethodError]]).

A failed static initializer first throws `ExceptionInInitializerError` (wrapping a non-`Error` cause). The class is then erroneous; a later use throws `NoClassDefFoundError`. Both sit under `LinkageError` ([[What happens if you use a class after ExceptionInInitializerError]]).

`Class.forName("…")` when the name cannot be loaded is the checked `ClassNotFoundException`, not a `LinkageError` ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]], [[What are common examples of checked exceptions in Java]]).

```d2
direction: down
err: Error {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
le: LinkageError {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
ncdfe: NoClassDefFoundError {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
eiie: ExceptionInInitializerError {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
icce: IncompatibleClassChangeError {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
nsme: NoSuchMethodError {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
cnfe: ClassNotFoundException {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
ex: Exception {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
err -> le
le -> ncdfe
le -> eiie
le -> icce
icce -> nsme
ex -> cnfe
```

**Fig. 1.** `LinkageError` is an `Error`. Reflective load-by-name is a checked `Exception`.

```java
class Demo {
    static Class<?> byName(String name) throws ClassNotFoundException {
        return Class.forName(name);
    }
}
```

**Listing 1.** Missing name through `Class.forName` is `ClassNotFoundException` (checked). A compile-time dependency that is gone or binary-incompatible at run time is a `LinkageError` subclass, not this method’s `throws`.

> [!warning] `ClassNotFoundException` is not a `LinkageError`
> Interview lists mix “class not found” wording. Reflective load-by-name is a checked `Exception`. `NoClassDefFoundError` is the `Error` when the VM cannot find a class the running code already depends on.

> [!warning] Failed `<clinit>` is two types, both under `LinkageError`
> First use: `ExceptionInInitializerError`. Later use of that same failed class: `NoClassDefFoundError`. Catching only one of them is a common trap ([[What happens if you use a class after ExceptionInInitializerError]]).

> [!tip] Interview answer
> **`LinkageError` is an unchecked `Error` when a class’s dependency is missing or incompatibly changed at run time.** Typical children are `NoClassDefFoundError`, `ExceptionInInitializerError`, and `NoSuchMethodError`. `ClassNotFoundException` is a different, checked type from reflective load-by-name.
