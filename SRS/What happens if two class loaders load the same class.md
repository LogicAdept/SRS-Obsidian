<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What happens if two class loaders load the same class

> [!abstract] Short answer
> You get two different runtime `Class` objects and two independent sets of static state for one binary name. Type identity in the JVM is the pair (binary name, defining loader): the name matches, the loaders differ, so the types differ — instances of one cannot be cast to the other, and the attempt throws `ClassCastException` naming the same class twice.

## Identity is the pair (binary name, defining loader)

The spec distinguishes the two roles a loader can play: if a loader loads a class directly, it defines the class and is its defining loader; whether a class was loaded directly or through delegation, the loader that started the load is an initiating loader. `getClassLoader()` on the loaded class returns the defining loader. Two `Class` objects produced by different defining loaders compare unequal — `Class` equality is identity, and `instanceof` or `isInstance` check the runtime type, so a check against one fails for instances of the other even though `getName()` returns the same string.

## One loader defines a name only once

Uniqueness is enforced per loader, in two places. `loadClass` starts with `findLoadedClass(String)` — the loader's own cache of already-defined names. Below that, the JVM checks it again at derivation: it determines whether that loader has already been recorded as an initiating loader of a class denoted by that name, and if so the derivation attempt is invalid and throws a `LinkageError`. So one loader cannot define the same name twice; two loaders define it as two types.

```java
URL jar = new File("payment.jar").toURI().toURL();
URLClassLoader a = new URLClassLoader("a", new URL[]{jar}, null); // no parent: isolated
URLClassLoader b = new URLClassLoader("b", new URL[]{jar}, null);

Class<?> ca = a.loadClass("app.Payment");
Class<?> cb = b.loadClass("app.Payment");

System.out.println(ca.getName());       // app.Payment
System.out.println(ca == cb);           // false
System.out.println(ca.equals(cb));      // false

Object obj = cb.getDeclaredConstructor().newInstance();
System.out.println(ca.isInstance(obj)); // false
// (Payment) obj;                       // ClassCastException: app.Payment cannot be
                                        // cast to app.Payment  (loader b -> loader a)
```

**Listing 1.** Same jar, same binary name, two defining loaders: two `Class` objects, and a cross-cast that fails while the class name looks identical.

```d2
direction: right
la: "loader a" {
  width: 120
  height: 50
  style.fill: "#e3f2fd"
}
lb: "loader b" {
  width: 120
  height: 50
  style.fill: "#fff3e0"
}
ca: "Class app.Payment\nstatics of a" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
cb: "Class app.Payment\nstatics of b" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
obj: "instance of cb" {
  width: 150
  height: 50
  style.fill: "#ffebee"
}
la -> ca: "defines"
lb -> cb: "defines"
cb -> obj
obj -> ca: "cast fails\nClassCastException" {
  style.stroke: "#c62828"
}
```

**Fig. 1.** The two `Class` objects are separate type roots: the cast edge from a `b`-defined instance toward the `a` type is rejected at runtime.

> [!warning] The message naming one class twice is the diagnostic
> `ClassCastException: app.Payment cannot be cast to app.Payment` is not a compiler or JVM bug — it is two defining loaders in one process. Fix it at load time, not at the cast: keep one copy of the library reachable through delegation ([[What is the Java classpath]] — two versions of one class on the classpath is silent breakage) or restructure the isolation deliberately ([[How would you explain Classloader parent delegation model]] — parent-first is the default, not a law).

> [!warning] Frameworks multiply this silently
> Every layer that defines classes — a plugin manager, a webapp container redeploying an old loader, OSGi bundles, test-isolation loaders — can hold its own copy of a name. Objects that cross such a boundary carry their defining loader with them, so stale loaders from a previous deployment keep whole object graphs alive.

> [!tip] Interview answer
> **Same binary name under two defining loaders is two types: two `Class` objects with `==` false, two static states, and `ClassCastException` on a cross-cast — with the same class name on both sides of the message. A single loader is prevented from defining a name twice by `findLoadedClass` and a `LinkageError` at derivation. Identity is (name, loader), which is exactly why delegation exists.**

