<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Class #Java/JVM/ClassLoaders #Java/Versions/9 #SRS

# What does `Class.forName` do and what are its overloads?

> [!abstract] Short answer
> **It returns the `Class` for a binary name, locating and loading it through a class loader.** The one-argument form is `forName(name, true, callerLoader)`: **load and initialize**. The three-argument form lets you choose initialization and the loader (`null` = bootstrap). Since 9, `forName(Module, name)` loads **without linking or `<clinit>`** and returns **`null`** if the name is missing — not `ClassNotFoundException`.

## Three overloads

```d2
direction: down
name: "binary name" {
  width: 160
  height: 40
}
one: "forName(String)\ninit = true, caller loader" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
three: "forName(name, initialize, loader)" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
mod: "forName(Module, name)\nno link, no <clinit>, null if missing" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
name -> one
name -> three
name -> mod
```

**Fig. 1.** Same job (name → `Class`), three control knobs: initialize, loader, module. None of them is `Foo.class` or `obj.getClass()` ([[How can you get the Class object in Java]], [[What is the difference between getClass and Class.forName]]).

**`forName(String className)`** — equivalent to `forName(className, true, currentLoader)` where `currentLoader` is the **defining loader of the caller**. No caller frame (JNI attached thread) → **system** class loader. `forName("X")` **initializes** `X`. Throws checked `ClassNotFoundException` if the name cannot be located; also `LinkageError` / `ExceptionInInitializerError` per JLS 12.2–12.4 ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

**`forName(String name, boolean initialize, ClassLoader loader)`** since 1.2 — **binary name** (or array encoding). The given loader loads the type; `loader == null` means the **bootstrap** loader. Initialization runs only if `initialize` is true and the class is not already initialized. A failing `<clinit>` is `ExceptionInInitializerError`. `SecurityException` if a security manager is present, `loader` is null, the caller’s loader is not null, and `RuntimePermission("getClassLoader")` is denied.

This overload **cannot** return the `Class` objects for primitives, `void`, hidden classes, or arrays whose element type is hidden. `forName("int")` looks for a user class named `int`, not `int.class`. Arrays use `Class.getName()` encoding: `"[Ljava.lang.String;"`, `"[[[I"` for `int[][][]`. Nested types use `$`. `getName()` on the result equals the string you passed. Loading an array `"[L`N`;"` loads element type N **without initializing it**, even if `initialize` is true ([[How can you determine if a Class represents an array]]).

**`forName(Module module, String name)`** since 9 — binary name in that module. **Does not link** and **does not run** the class initializer. Missing type → **`null`**, not `ClassNotFoundException`. Does not support array types. Does not check whether the caller may access the class.

```java
class Load {
    static Class<?> plugin() throws ClassNotFoundException {
        return Class.forName("com.example.MyPlugin"); // init + caller loader
    }

    static Class<?> listed(ClassLoader loader) throws ClassNotFoundException {
        return Class.forName("com.example.MyPlugin", false, loader);
    }

    static Class<?> nested() throws ClassNotFoundException {
        return Class.forName("java.lang.Character$UnicodeBlock");
    }
}
```

**Listing 1.** One-arg initializes. Three-arg `false` locates and loads without running `<clinit>` (initialization implies linking; skip it until first active use). Construction is a later step ([[How can you create an instance of a class using reflection]]).

A newly loaded JDBC `Driver` is specified to call `DriverManager.registerDriver` — typically from `<clinit>`, which is why the old `Class.forName("…Driver")` pattern registered a driver. `DriverManager` itself also loads `java.sql.Driver` **service providers** (and `jdbc.drivers`) during its initialization, so modern code often never calls `forName` for that.

> [!warning] One-arg always initializes
> That is the feature and the foot-gun. A static block that talks to the network or registers a singleton runs on `forName(name)`. Use `initialize = false` when you only need the `Class` object. Initialization later still happens on first active use.

> [!warning] `ClassNotFoundException` is not the only failure
> Missing name → checked CNFE (except the `Module` overload’s `null`). Bad linkage → `LinkageError`. Failed `<clinit>` → `ExceptionInInitializerError`; a later use of that class is `NoClassDefFoundError`. Hidden classes are invisible to `forName`.

> [!tip] Interview answer
> **One-arg `forName` loads and initializes with the caller’s class loader — it is the three-arg call with `true`.** Three-arg chooses loader and whether to run `<clinit>`; `null` loader is bootstrap. **The Java 9 `forName(Module, name)` does not initialize and returns `null` on miss, not `ClassNotFoundException`.**
