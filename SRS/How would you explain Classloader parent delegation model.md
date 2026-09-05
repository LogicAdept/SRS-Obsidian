<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# How would you explain Classloader parent delegation model?

> [!abstract] Short answer
> **Default `ClassLoader.loadClass` is parent-first: already-loaded, then the parent (bootstrap if parent is `null`), then this loader’s `findClass`.** That is an API convention, not a JVM mandate — a loader may define a type itself or delegate. The usual built-in chain is application → platform → bootstrap. A successful delegate still makes the **requester** an *initiating* loader; the loader that `defineClass`s (or bootstrap) is the **defining** loader. A type is the pair (binary name, defining loader).

## What “parent-first” actually runs

Every `ClassLoader` instance has a **parent** used for delegation (`getParent()`). `new ClassLoader()` uses `getSystemClassLoader()` as that parent. `new ClassLoader(parent)` lets you pick; `parent == null` means bootstrap. Bootstrap itself is not a `ClassLoader` object and has no parent.

The default `loadClass(name, resolve)` search is:

1. `findLoadedClass(name)` — has *this* loader already been recorded as an **initiating** loader of that binary name?
2. `parent.loadClass(name)` — if `parent` is `null`, the VM’s bootstrap loader.
3. `findClass(name)` — empty by default (`ClassNotFoundException`). Override this, then `defineClass` ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

If step 2 succeeds, step 3 never runs. If `resolve` is true, `resolveClass` then **links**. One-arg `loadClass(name)` is `loadClass(name, false)`. The spec text is **usually** parent-first, not always.

```d2
direction: down
req: "child.loadClass(N)" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
cache: "findLoadedClass(N)" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
par: "parent.loadClass(N)\nnull → bootstrap" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
self: "findClass(N) → defineClass" {
  width: 260
  height: 45
  style.fill: "#f3e5f5"
}
req -> cache
cache -> par: "miss"
par -> self: "parent cannot find N"
```

**Fig. 1.** Parent-first on one loader. Recursion walks to bootstrap; `findClass` runs only on the way back when no ancestor defined `N` ([[How would you explain the Java class loader]]).

```d2
direction: right
app: "application\n\"app\"" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
plat: "platform\n\"platform\"" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
boot: "bootstrap\nnull" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
app -> plat: "parent (or ancestor)"
plat -> boot: "parent"
```

**Fig. 2.** Built-in chain since 9. There is no `lib/ext` search. Platform is the parent **or an ancestor** of the system loader; it may also **delegate to the application loader** when an upgraded platform module reads an application module.

The JVM asks a loader `L` to locate `N`. `L` may **define** `N` or **delegate**. If the VM asked `L1` and `L2` defined the class, both are initiating loaders of that type; loaders strictly between them in the chain are not. `findLoadedClass` looks at that initiating record, not “did I define it?”.

Why parent-first exists:

- One defining loader per name **along a well-behaved chain**, so `java.lang.String` from application code is still bootstrap’s `String`.
- `defineClass`: a name that begins with `java.` may be defined only by the **platform loader or its ancestors**; any other loader gets `SecurityException`. Parent-first is how application code still *resolves* those names without *defining* them.
- Well-behaved loaders: the same name from the same loader always yields the same `Class`; if `L1` delegates `C` to `L2`, they must agree on the `Class` objects for `C`’s supertypes, field types, and method types (loader constraints enforce this).

```java
class DelegationWalk {
    static String chain() {
        StringBuilder sb = new StringBuilder();
        for (ClassLoader cl = ClassLoader.getSystemClassLoader(); cl != null; cl = cl.getParent()) {
            sb.append(cl.getName()).append(" -> ");
        }
        return sb.append("bootstrap").toString();
    }

    static Class<?> throughChild(String binaryName) throws ClassNotFoundException {
        ClassLoader child = new ClassLoader() {}; // parent = system loader
        return child.loadClass(binaryName);       // never hits findClass for java.*
    }
}
```

**Listing 1.** Typical printed chain is `app -> platform -> bootstrap`. `throughChild("java.lang.String")` is defined by bootstrap; the anonymous child is only an initiating loader. Override **`findClass`**, not `loadClass`, to stay on this model. `Class.forName(name)` still uses the **caller’s defining loader**, not “the child’s parent” ([[What does Class.forName do and what are its overloads]]).

Custom loaders (plugins, extra code sources) pass an explicit parent — usually the system loader, or `getPlatformClassLoader()` when the child must see all platform types. Graphs that are **not** a tree must `registerAsParallelCapable()`; otherwise `loadClass` holds the loader lock for the whole search and cross-delegation deadlocks.

> [!warning] Parent-first is the default, not a law
> Override `loadClass` and you skip the documented order (child-first, filtered packages, graphs). The VM still allows a loader to define a class itself. What you cannot do is `defineClass` a `java.*` name unless you *are* the platform loader or an ancestor — `SecurityException`. Parent `null` also hides platform types that bootstrap does not define.

> [!warning] Same binary name, two defining loaders
> Parent-first prevents the *child* from defining a name the *parent* already owns. Two siblings that each `defineClass` the same bytes still produce two types. `a.loadClass(N) == b.loadClass(N)` is true when both delegate to the same defining ancestor; it is false when each defines `N`. Casts across that boundary are `ClassCastException`.

> [!tip] Interview answer
> **Parent-first means `findLoadedClass`, then parent (bootstrap if `null`), then `findClass` — so JDK types keep a single defining loader.** That is `ClassLoader`’s default, not something the JVM forces on every loader. **A type is still (name, defining loader); override `findClass` to participate, `loadClass` only if you mean to change delegation.** Since 9 the middle parent is platform, not `lib/ext`.
