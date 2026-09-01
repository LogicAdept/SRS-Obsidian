<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #SRS

# How can you get the Class object in Java?

> [!abstract] Short answer
> **Three everyday paths: a class literal (`String.class`), `obj.getClass()`, and `Class.forName(binaryName)`.** `.class` is a compile-time expression for a named type (including primitives, arrays, and `void`). `getClass()` is the **runtime** class of a non-null instance. `forName` loads by **binary name** and, in the one-argument form, **initializes** the class. There is no public `Class` constructor.

## Literal, instance, or name

`Class` objects are created by the VM (and by `Lookup.defineClass` / `defineHiddenClass`), not by application code calling `new Class()`. The usual ways to *obtain* one already in hand:

```d2
direction: down
need: "Need a Class<?>" {
  width: 180
  height: 45
}
lit: "Type.class" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
rt: "instance.getClass()" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
fn: "Class.forName(name)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
need -> lit: "type known in source"
need -> rt: "have an object"
need -> fn: "name is a String"
```

**Fig. 1.** Compile-time type vs runtime class vs load-by-name. They are not interchangeable ([[What is the difference between getClass and Class.forName]], [[What is the Class class in Java reflection]]).

```java
class Holder {}

class Paths {
    static Class<Holder> literal() {
        return Holder.class;
    }

    static Class<? extends Holder> ofInstance(Holder h) {
        return h.getClass();
    }

    static Class<?> byName() throws ClassNotFoundException {
        return Class.forName("Holder");
    }
}
```

**Listing 1.** Same `Holder` via literal, instance, and binary name. `forName` declares checked `ClassNotFoundException`.

A **class literal** is `TypeName.class`, `int.class`, `String[].class`, or `void.class`. It evaluates to the `Class` object for that type as defined by the current instance’s defining loader (JLS 15.8.2). The type of `C.class` is `Class<C>`; the type of `int.class` is `Class<Integer>` (boxing of the primitive); `void.class` is `Class<Void>`.

`Object.getClass()` returns the **runtime** class of `this` — the `Class` locked by `static synchronized` methods of that class. The result type is `Class<? extends |X|>` where `|X|` is the erasure of the static type, so `Number n = 0; Class<? extends Number> c = n.getClass();` needs no cast. A variable typed `Holder` may still return a **subclass** (or a proxy class). You cannot call it on `null`.

`Class.forName(String)` is `Class.forName(name, true, currentLoader)`: binary name, **initialize**, caller’s loader (system loader if there is no caller frame). `forName("X")` runs `X`’s initializer. The three-argument form can pass `initialize = false` and an explicit loader (`null` = bootstrap). Nested types use `$` (`java.lang.Character$UnicodeBlock`). Array classes use the `getName` encoding (`"[Ljava.lang.String;"`, `"[[[I"`) ([[How can you determine if a Class represents an array]], [[What does Class.forName do and what are its overloads]]).

A Java 9+ overload `forName(Module, String)` does **not** initialize, returns **`null`** if missing (not `ClassNotFoundException`), and does not check accessibility.

Once you have the `Class`, construction is a separate step ([[How can you create an instance of a class using reflection]]).

> [!warning] `forName` is not `.class` for primitives
> `Class.forName("int")` does **not** yield `int.class`. The method cannot return the `Class` objects for primitives, `void`, or hidden classes; a name like `I` is treated as a user class in the unnamed package. Use `int.class` / `void.class`. Default `forName` also **initializes**, so a failing `<clinit>` is `ExceptionInInitializerError`, and a later use can be `NoClassDefFoundError` ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

> [!warning] `getClass()` is the live type
> `Holder.class` is the named type in source. `h.getClass()` is whatever was actually allocated. That is the point of the method — and why a factory typed as an interface still reveals the concrete (or proxy) class.

> [!tip] Interview answer
> **`.class` when the type is in the source, `getClass()` when you have an instance, `Class.forName` when you have a binary name.** `forName` throws checked `ClassNotFoundException` and, in the one-arg form, initializes the class. **Do not use `forName` for `int` or `void` — those are `int.class` and `void.class`.**
