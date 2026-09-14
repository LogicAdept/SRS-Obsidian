<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #Java/Language/Reflection/Class #SRS

# What is the difference between loadClass and Class.forName in Java

> [!abstract] Short answer
> `loader.loadClass(name)` only locates and loads: it is `loadClass(name, false)` — no linking step, no `<clinit>`. One-arg `Class.forName(name)` is `forName(name, true, caller's defining loader)`: it loads and causes the class to be initialized. Both delegate; they differ in which loader they ask and how far the class lifecycle is advanced.

## `loadClass`: load only

`loadClass(String)` is invoked by the virtual machine itself to resolve class references, and invoking it is equivalent to invoking `loadClass(name, false)`. The two-arg default implementation checks `findLoadedClass`, delegates to the parent (a `null` parent falls back to the loader built into the virtual machine), then calls `findClass`; the class is resolved only if the `resolve` flag is true. A `loadClass(name)` call therefore hands you a `Class` object whose static initializers have not run — you get the type without any of its side effects.

## `forName`: load plus initialize

`Class.forName(className)` is equivalent to `Class.forName(className, true, currentLoader)`, where `currentLoader` denotes the defining class loader of the current class — and a call to `forName("X")` causes the class named X to be initialized. The three-arg form spells both knobs out: the given class loader is used to locate and load the class (a `null` loader means the bootstrap loader), and the class is initialized only if the `initialize` parameter is true and it has not been initialized earlier. Initialization therefore also implies the class has been verified and prepared ([[What happens during the linking phase of class loading in the JVM]]).

```java
ClassLoader loader = Thread.currentThread().getContextClassLoader();

Class<?> a = loader.loadClass("com.example.Plugin");
// loaded by the loader you chose; <clinit> has NOT run

Class<?> b = Class.forName("com.example.Plugin");
// forName(name, true, caller's defining loader): <clinit> HAS run

Class<?> c = Class.forName("com.example.Plugin", false, loader);
// loaded via the chosen loader, no initialization
```

**Listing 1.** Three call shapes, three lifecycle depths: load, load-and-initialize, load-without-initialize.

```d2
direction: right
lc: "loadClass(name)" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
fn2: "forName(name, false, loader)" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
fn1: "forName(name)" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
load: "loaded" {
  width: 120
  height: 55
  style.fill: "#e3f2fd"
}
init: "initialized\n(<clinit> ran)" {
  width: 160
  height: 55
  style.fill: "#e8f5e9"
}
lc -> load
fn2 -> load
fn1 -> load
fn1 -> init
```

**Fig. 1.** All three produce a `Class`; only one-arg `forName` reaches initialization, which is why it alone runs static initializers.

> [!warning] One-arg `forName` executes code as a side effect
> Loading a class is pure lookup, but initialization runs `<clinit>` — historically how JDBC drivers self-registered on `Class.forName("...Driver")` ([[How do you register a JDBC driver]]). If the static block does anything heavy or stateful, `forName` triggers it and `loadClass` does not. The second trap: one-arg `forName` uses the defining loader of the caller, so from a framework class it cannot see application classes unless you pass the loader explicitly ([[What is the thread context class loader in Java]] — the standard workaround).

> [!tip] Interview answer
> **`loadClass` loads; one-arg `forName` loads and initializes. `loadClass(name)` equals `loadClass(name, false)` — no resolution step, no `<clinit>`. `forName(name)` equals `forName(name, true, caller loader)` — it initializes, running static initializers, and takes the loader from the calling class unless you pass one. Use `forName(name, false, loader)` or `loadClass` when you want the type without side effects.**

