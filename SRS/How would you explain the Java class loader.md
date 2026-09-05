<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# How would you explain the Java class loader?

> [!abstract] Short answer
> **A class loader is the object that, given a binary name, locates or produces class-file bytes and hands them to the VM to derive a `Class`.** There is no public `Class` constructor — the VM creates `Class` objects via `ClassLoader.defineClass` (or `Lookup.defineClass` / `defineHiddenClass`). Three built-in loaders: bootstrap (`null`), platform, application. Default search is parent-first. Then **link** (verify, prepare, optionally resolve) and **initialize** (`<clinit>`). A type is the pair (binary name, defining loader).

## What the loader is

`java.lang.ClassLoader` is abstract. A typical implementation turns a binary name into a file (or other bytes) and calls `defineClass`. Every `Class` holds a reference to the loader that **defined** it. `Class.getClassLoader()` returns that loader; implementations use `null` for bootstrap, and `null` also for primitive types and `void`. Array classes are not defined by `defineClass`: the VM creates them, and `getClassLoader()` on an array is the element type’s loader (`null` if the element is primitive).

The VM asks a loader to locate a name. That loader may **define** the class or **delegate**. The requester is an *initiating* loader; the one that `defineClass`s (or bootstrap) is the *defining* loader.

```d2
direction: down
name: "binary name" {
  width: 160
  height: 40
}
cl: "ClassLoader\nfind bytes → defineClass" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
vm: "VM derives Class\nin the method area" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
name -> cl
cl -> vm
```

**Fig. 1.** Loader supplies a binary; the VM creates the `Class`. Hidden classes from `Lookup.defineHiddenClass` are not discoverable by `loadClass` / `forName`.

## Built-in loaders

- **Bootstrap** — VM-built-in, typically `null`, no parent. Core types in a platform-dependent way. Not a `ClassLoader` you construct. Not every `java.*` type is bootstrap-defined; some SE types moved to platform (Java 9).
- **Platform** — `ClassLoader.getPlatformClassLoader()` (since 9, name `"platform"`). Java SE APIs, their implementations, and JDK run-time types defined here or by an ancestor. Replaces the old extension loader.
- **System / application** — `ClassLoader.getSystemClassLoader()` (name `"app"`). Class path, module path, JDK tools. Platform is its parent **or ancestor**. Default parent of `new ClassLoader()`.

Before 9 the middle loader was **extension** (`lib/ext`, `java.ext.dirs`) and core libraries lived in `rt.jar`. JEP 220 removed both. JEP 261 renamed the leftover middle loader to platform and stopped using `URLClassLoader` for it or for the application loader.

```d2
direction: right
boot: "bootstrap\nnull" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
plat: "platform" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
app: "application" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
app -> plat: "parent"
plat -> boot: "parent"
```

**Fig. 2.** Parent-first walks this chain, then `findClass` on the way back ([[How would you explain Classloader parent delegation model]]).

Default `loadClass(name, resolve)`: `findLoadedClass` → parent (`null` → bootstrap) → `findClass`. If `resolve` is true, `resolveClass` **links**. One-arg `loadClass(name)` is `loadClass(name, false)`: locate, do not link. Override `findClass`, not `loadClass`, to stay parent-first. A loader **usually** delegates first — not always (platform may delegate to application for upgraded modules).

## Load, link, initialize

**Loading** finds a binary and constructs a `Class`. **Linking:** verification (`VerifyError` if the binary is illegal); preparation (create `static` fields and set **defaults** — no Java code; explicit static initializers are not this step); resolution of symbolic references (lazy per use or eager at verify; uses the referring class’s defining loader). A class is fully loaded before it is linked, and fully verified and prepared before it is initialized.

**Initialization** runs `<clinit>`. Superclasses (and superinterfaces that declare default methods) first. Triggers: `new`, a non-constant static field, a static method, one-arg `Class.forName`, some reflective APIs, VM startup of `main`. Failed `<clinit>` is `ExceptionInInitializerError`; a later use is `NoClassDefFoundError` ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

Implicit load: bytecode that first uses a name asks the referring class’s defining loader. Explicit: `loadClass` / `forName` ([[What does Class.forName do and what are its overloads]], [[How can you get the Class object in Java]]).

```d2
direction: right
load: "Load\nbinary → Class" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
link: "Link\nverify · prepare · resolve?" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
init: "Initialize\n<clinit>" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
load -> link
link -> init
```

**Fig. 3.** Order is fixed; **when** other names are linked is an implementation choice, as long as errors surface at a use of the bad reference.

```java
class WhichLoader {
    static ClassLoader of(Class<?> type) {
        return type.getClassLoader(); // null: bootstrap, or primitive/void
    }

    static ClassLoader application() {
        return ClassLoader.getSystemClassLoader();
    }

    static ClassLoader platform() {
        return ClassLoader.getPlatformClassLoader();
    }

    static Class<?> locate(String binaryName) throws ClassNotFoundException {
        return application().loadClass(binaryName); // no <clinit>
    }

    static Class<?> locateAndInit(String binaryName) throws ClassNotFoundException {
        return Class.forName(binaryName); // init + caller’s defining loader
    }
}
```

**Listing 1.** Who defined a type, the application loader, locate without init vs `forName` with init. `String.class.getClassLoader()` is `null`; `platform().getParent()` is typically `null` (bootstrap). Three-arg `forName(name, false, loader)` skips `<clinit>`.

Subclass `ClassLoader` when bytes are not on the class/module path, or when you need a **separate defining loader** you can drop (plugins, reload). That is a new `Class` for the same name, not an in-place edit ([[How would you explain Java class loaders and dynamic class loading]]). `defineClass` of a `java.*` name from a non-platform loader is `SecurityException`. A custom loader whose parent is `null` does not see every platform class — parent it on `getPlatformClassLoader()`.

> [!warning] `getClassLoader() == null` is two different facts
> Bootstrap-defined types return `null`. So do `int.class` and `void.class`, which were never loaded by a class loader. `Integer.class.getClassLoader()` is not `int.class.getClassLoader()`’s wrapper equivalent — one is a reference type from bootstrap, the other is a primitive `Class`.

> [!warning] `loadClass` is not `forName`
> `loadClass(name)` is `loadClass(name, false)`: find the `Class`, do not link, do not run `<clinit>`. One-arg `Class.forName(name)` is `forName(name, true, callerLoader)` and **does** initialize. `forName("int")` is not `int.class`.

> [!warning] One name is not one type
> Parent-first keeps `java.lang.String` unique along a well-behaved chain. Two defining loaders that each `defineClass` the same bytes still produce two types; a cast between them is `ClassCastException`. `a.loadClass(N) == b.loadClass(N)` only when they share the defining ancestor.

> [!warning] Pre-Java 9 loader folklore
> There is no `lib/ext` / `java.ext.dirs` search, no `rt.jar`, and `getSystemClassLoader()` is not a `URLClassLoader`. Internal names such as `Launcher$AppClassLoader` are not the API.

> [!tip] Interview answer
> **A class loader maps a binary name to bytes and the VM turns that into a `Class` — you never `new` a `Class`.** Built-in chain is bootstrap (`null`), platform, application; default `loadClass` is already-loaded, then parent, then `findClass`. **Loading makes the `Class`; linking verifies and prepares statics to defaults; initialization runs `<clinit>`. The run-time type is (name, defining loader).** `forName` initializes; `loadClass` does not.
