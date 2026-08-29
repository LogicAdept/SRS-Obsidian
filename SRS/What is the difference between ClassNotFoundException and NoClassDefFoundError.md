<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #Java/Exceptions/Hierarchy #Java/Exceptions/Error #Java/Exceptions/Checked #SRS

# What is the difference between `ClassNotFoundException` and `NoClassDefFoundError`?

> [!abstract] Short answer
> **`ClassNotFoundException` is a checked exception when you load a class by name and it cannot be found.** **`NoClassDefFoundError` is an `Error` when the JVM needs a class while resolving or initializing another type and the definition is gone — or the class is left erroneous after a failed static initializer.** Rule of thumb: CNFE = you asked by string; NCDFE = a compile-time dependency (or a later use of a failed class) cannot be loaded.

## By-name lookup versus linkage

`ClassNotFoundException` extends `ReflectiveOperationException` (hence `Exception`). `Class.forName`, `ClassLoader.loadClass`, and `ClassLoader.findSystemClass` throw it when no definition exists for that name. You must catch or declare it ([[What are common examples of checked exceptions in Java]], [[What happens if you neither catch nor declare a checked exception]]).

`NoClassDefFoundError` extends `LinkageError`, hence `Error`. It is thrown when the VM or a class loader cannot find a class needed as part of a normal call or `new` — typically a type that existed when the caller was compiled but is missing at run time (JAR not deployed). After a static initializer fails, the class is erroneous; a later use throws `NoClassDefFoundError`, not a second `ExceptionInInitializerError` ([[What is LinkageError]], [[What happens if you use a class after ExceptionInInitializerError]], [[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]]).

`catch (Exception e)` matches CNFE and misses NCDFE ([[Does catch Exception also catch Error]]).

`Class.forName` is not “CNFE only”: it also throws `LinkageError` (including `NoClassDefFoundError`) if linkage fails, and `ExceptionInInitializerError` if this call’s initialization fails.

```d2
direction: down
throwable: Throwable {
  width: 180
  height: 40
}
ex: Exception {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
err: Error {
  width: 180
  height: 40
  style.fill: "#ffebee"
}
roe: ReflectiveOperationException {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
le: LinkageError {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
cnfe: ClassNotFoundException {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
ncdfe: NoClassDefFoundError {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
throwable -> ex
throwable -> err
ex -> roe
roe -> cnfe
err -> le
le -> ncdfe
```

**Fig. 1.** Same “class not found” wording; checked `Exception` versus `Error`.

```java
class Demo {
    static Class<?> loadByName() throws ClassNotFoundException {
        return Class.forName("com.mysql.cj.jdbc.Driver");
    }
}
```

**Listing 1.** Missing driver JAR on a **by-name** load is `ClassNotFoundException` (checked). A class compiled against `Helper` whose `Helper.class` is absent at run time is `NoClassDefFoundError` on the first `new Helper()` / static use — no `throws ClassNotFoundException` on that call site.

> [!warning] Same English, two types
> Interview tables that stop at “missing JAR” for both names skip the hierarchy. CNFE is checked. NCDFE is an `Error`. Catching `Exception` around `forName` does not catch a later `NoClassDefFoundError` from `new`.

> [!warning] Failed `<clinit>` looks like “class not found”
> First failure: `ExceptionInInitializerError`. Later use of that class: `NoClassDefFoundError`. The `.class` file can still be on disk ([[What happens if you use a class after ExceptionInInitializerError]]).

> [!tip] Interview answer
> **`ClassNotFoundException` is checked: you asked for a name with `Class.forName` or `loadClass` and it was not there.** **`NoClassDefFoundError` is an `Error` when the VM cannot find a class it already depended on, or when that class is left broken after a failed static initializer.** Do not treat them as the same “class not found” exception.
