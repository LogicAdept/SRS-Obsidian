<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# How would you explain Java class loaders and dynamic class loading?

> [!abstract] Short answer
> **The VM does not load every type up front. A class loader locates a binary for a name and the VM derives a `Class`; later bytecode, `loadClass`, or `forName` can pull in more types.** Built-in loaders cover bootstrap / platform / application. You subclass `ClassLoader` to take bytes from somewhere else (network, generated, encrypted, a plugin tree) or to **drop a loader** and define a fresh `Class` for the same name. Reloading is a new defining loader, not an in-place edit of the old `Class`.

## Dynamic loading

Loading is finding a binary and constructing a `Class`. Linking (verify, prepare, optionally resolve) and initialization (`<clinit>`) follow. The VM starts by loading the initial class, linking it, initializing it, and calling `main`; further types appear when something actually uses them, or when you ask by name ([[How would you explain the Java class loader]]).

Explicit asks: `ClassLoader.loadClass` (no `<clinit>` by default) and `Class.forName` (one-arg **does** initialize) ([[What does Class.forName do and what are its overloads]]). Implicit: a symbolic reference in a class the VM is resolving. Different `ClassLoader` subclasses may cache, prefetch, or load a group together; they must still report failure only at a point that would have loaded without prefetch.

A type is `<binary name, defining loader>`. Two loaders that each `defineClass` the same bytes produce two types.

## Why a custom `ClassLoader`

The VM supplies bootstrap (`null`), platform, and application. User-defined loaders exist to **change where bytes come from** and **who defines** the resulting `Class`. The VM spec’s examples are: download across a network, generate on the fly, extract from an encrypted file. Isolation follows: a plugin’s types never become the parent’s types, so you can unload the plugin by dropping every live reference to that loader.

```d2
direction: down
need: "Need a Class the built-in chain will not define" {
  width: 340
  height: 50
}
src: "Other bytes\nnetwork · generated · encrypted · plugin dir" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
iso: "Separate defining loader\nunload / replace the tree" {
  width: 340
  height: 55
  style.fill: "#fff3e0"
}
need -> src
need -> iso
```

**Fig. 1.** Subclass when the source is not class path / module path, or when you must throw the *loader* away later. Default search is still parent-first unless you override `loadClass` ([[How would you explain Classloader parent delegation model]]).

Override **`findClass`**, read or produce bytes, call **`defineClass`**. Leave `loadClass` alone to keep parent-first. `defineClass` a name starting with `java.` unless you are the platform loader or an ancestor → `SecurityException`. Non-tree graphs must `registerAsParallelCapable()`.

```java
class BytesLoader extends ClassLoader {
    private final String binaryName;
    private final byte[] classFile;

    BytesLoader(ClassLoader parent, String binaryName, byte[] classFile) {
        super(parent); // null parent = bootstrap; platform types may be invisible
        this.binaryName = binaryName;
        this.classFile = classFile;
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        if (!binaryName.equals(name)) {
            throw new ClassNotFoundException(name);
        }
        return defineClass(name, classFile, 0, classFile.length);
    }
}
```

**Listing 1.** Parent-first custom loader: `loadClass` unchanged, `findClass` defines from a byte array you obtained however you like. A second `BytesLoader` with the same bytes defines a **different** `Class`.

Reload: a class may be unloaded **only if its defining loader is reclaimable**. Bootstrap-defined types are never unloaded. You cannot “swap” `Plugin` inside the application loader; well-behaved loaders return the same `Class` for the same name forever. The working pattern is: new child loader, define the new bytes, drop all references to the old loader (and its types and instances) so the GC can take it. Reloading is **not** transparent: `static` state, `<clinit>` side effects, `native` state, and `Class` identity/`hashCode` all change.

That is what Spring Boot DevTools does for *restart*: a disposable `RestartClassLoader` (parent-**last** for its URLs) holds project classes; third-party jars stay in a base loader; on restart the restart loader is thrown away and a new one is created. It is not the same as JVM TI `Instrumentation.redefineClasses` (fix-and-continue / agents): that **replaces bytes of an existing `Class`**, does not run initializers, leaves `static` fields and live instances as they were, and lets active stack frames keep the old bytecodes. Unsupported schema changes fail; primitives and arrays are never modifiable.

```d2
direction: right
cl: "New ClassLoader\ndefineClass again" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
gone: "old loader unreachable\nunload allowed" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
redef: "redefineClasses\nsame Class object" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
keep: "no <clinit>\nstatics and instances kept" {
  width: 220
  height: 70
}
cl -> gone
redef -> keep
```

**Fig. 2.** Two different “hot” stories. Only the left one is a class-loader feature.

> [!warning] Same name in the parent is not a new type
> `loadClass` that stays parent-first will return the parent’s `Class` and never call your `findClass`. Isolation and reload need either a name the parent will not define, or a deliberate child-first `loadClass` (and then two types named `Plugin` if some other loader also defined it). Casts across defining loaders are `ClassCastException`.

> [!warning] `redefineClasses` is not a custom `ClassLoader`
> Agents may patch an already loaded class under JVM TI rules. That does not unload anything, does not create a second `Class`, and does not re-run `<clinit>`. Application reload is a **new defining loader** after the old one is unreachable. A loader that still has live instances, threads, or a parent pointing at it will not let those classes go.

> [!tip] Interview answer
> **Dynamic loading means the VM creates `Class` objects on demand through a class loader — built-in chain for the JDK and class path, your subclass for other bytes or for isolation.** Custom loaders override `findClass` and `defineClass`; reload means throw the defining loader away, because a `Class` is stuck to that loader for its lifetime. **Parent-first is the default; parent-last is a choice when you must hide the parent’s copy of a name.**
