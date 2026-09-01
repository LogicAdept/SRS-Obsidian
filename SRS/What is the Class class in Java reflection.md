<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Class #SRS

# What is the Class class in Java reflection?

> [!abstract] Short answer
> **`java.lang.Class` is the runtime stand-in for a type: a class, an interface, an array, a primitive, or `void`.** Reflection starts here. Its methods expose name, members, and super types from the `class` file (and a few loading-time facts such as `getModule()`). There is **no public constructor**; the VM creates `Class` objects. Since 1.0.

## The type object, not `java.lang.reflect.Class`

`Class` lives in **`java.lang`**. Instances “represent classes and interfaces in a running Java application.” An enum and a record are kinds of class; an annotation type is a kind of interface. Every array has a `Class` **shared by all arrays with the same element type and number of dimensions** (length is not part of the type). `int.class` and `void.class` are `Class` objects too ([[How can you get the Class object in Java]], [[How can you determine if a Class represents an array]]).

The VM builds a `Class` when bytes become a type: `ClassLoader.defineClass`, `Lookup.defineClass`, or `Lookup.defineHiddenClass`. Application code obtains one already made: a class literal (`Foo.class`, JLS 15.8.2), `obj.getClass()`, or `Class.forName` ([[What does Class.forName do and what are its overloads]]).

```d2
direction: down
c: "Class<?>" {
  width: 160
  height: 45
}
meta: "Name, module,\nsuperclass, interfaces" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
mem: "Field / Method /\nConstructor" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
use: "newInstance / invoke / get / set" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
c -> meta
c -> mem
mem -> use
```

**Fig. 1.** `Class` is metadata **and** the factory for `java.lang.reflect` members. Those companion types do the actual get/set/invoke/construct ([[How can you invoke a method using reflection]], [[How can you access constructors using reflection]], [[How can you create an instance of a class using reflection]]).

Most methods describe the declaration: `getName()`, `isInterface()`, `isArray()`, `getSuperclass()` / `getInterfaces()`, `getMethods()` / `getDeclaredMethods()`, the same split for fields and constructors. `getDeclared*` sees members **declared** on that class at any access; `get*` (no `Declared`) sees **public** members, including inherited ones. Finding a private member is not the same as using it — that still needs `setAccessible` on the `Field` / `Method` / `Constructor` ([[What does setAccessible do in the Reflection API]]). `Array` creates and indexes arrays whose component type is a `Class`.

```java
void printClassName(Object obj) {
    System.out.println("The class of " + obj +
                       " is " + obj.getClass().getName());
}

void named() {
    Class<String> s = String.class;
    Class<Integer> i = int.class;   // primitive, not Integer.class
    Class<Void> v = void.class;
}
```

**Listing 1.** JavaDoc example: `getClass().getName()`. Literals cover reference types, primitives, arrays, and `void` — none of those call `new Class()`.

A hidden class (`Lookup.defineHiddenClass`) is still a `Class`, but its name is not a binary name: `forName` / `ClassLoader.loadClass` will not find it. Unnamed classes (preview in SE 21) still have a `Class`; `getSimpleName()` is `""` and `getCanonicalName()` is `null`.

> [!warning] You do not construct `Class`
> There is no public constructor. `new Class()` does not compile. If you do not already have a `Class`, you ask the VM (`getClass`, `.class`, `forName`), you do not allocate one.

> [!warning] One `Class` is not “the source file”
> `List.class` and `List<String>` at runtime share the same erasure `Class`. Array length is not in the `Class`. `Integer.class` is not `int.class`. Superclass/interface queries on `Class` are **direct**, not a flattened hierarchy ([[How do you inspect a class superclass and interfaces with reflection]]).

> [!tip] Interview answer
> **`Class` is the runtime type token — class, interface, array, primitive, or `void` — and the entry point for reflection.** You never `new` it; you get it from `.class`, `getClass()`, or `forName`, then ask it for `Field` / `Method` / `Constructor`. **It is `java.lang.Class`, not a type in `java.lang.reflect`.**
