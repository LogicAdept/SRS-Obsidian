<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/JVM/ClassLoaders #SRS

# What is the difference between getClass and Class.forName?

> [!abstract] Short answer
> **`getClass()` needs an instance and returns that object’s runtime `Class`. `Class.forName(name)` needs a binary name, is static, and in the one-argument form loads and initializes through the caller’s class loader.** You use `getClass` when you already have an object; you use `forName` when you only have a string. Neither is a class literal (`Foo.class`).

## Instance vs name

`Object.getClass()` is a `final` instance method: “the runtime class of this `Object`.” That `Class` is also the monitor for `static synchronized` methods of the represented class. The compile-time type of the result is `Class<? extends |X|>` where `|X|` is the erasure of the receiver, so `Number n = 0; Class<? extends Number> c = n.getClass();` needs no cast. A variable typed `List` can still return `ArrayList` — or a JDK dynamic proxy class ([[What is a dynamic proxy in Java reflection]], [[What is the Class class in Java reflection]]). There is no `getClass` on `null` (`NullPointerException`).

`Class.forName(String)` is static and equivalent to `forName(name, true, currentLoader)`: **binary name**, **initialize**, defining loader of the caller. No instance is required. Missing name → checked `ClassNotFoundException`. Failed `<clinit>` → `ExceptionInInitializerError` ([[What does Class.forName do and what are its overloads]], [[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

```d2
direction: down
have: "What you already have" {
  width: 220
  height: 40
}
gc: "obj.getClass()\nruntime class, no load-by-name" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
fn: "Class.forName(name)\nload + init, caller loader" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
have -> gc: "an object"
have -> fn: "a binary name"
```

**Fig. 1.** Same destination (`Class`), different inputs. `.class` is the third path when the type is written in the source ([[How can you get the Class object in Java]]).

| | `obj.getClass()` | `Class.forName(name)` |
|---|---|---|
| Kind | Instance, `final` | Static |
| Input | Live object | Binary name (nested `$`, arrays as `getName` encoding) |
| Result | Actual allocated type | Named type, after locate/load |
| Loader | Already attached to that `Class` | One-arg: **caller’s** defining loader |
| `<clinit>` | The instance’s class was already initialized | One-arg: **runs** it (`initialize = true`) |
| Failure | NPE if `obj` is null | Checked `ClassNotFoundException` (string overloads) |
| Primitives / `void` | No instance to call it on | **Cannot** return those `Class` objects (`forName("int")` is a user class named `int`) |

The three-argument `forName` can skip initialization and pick a loader (`null` = bootstrap). The Java 9 `forName(Module, name)` does not initialize and returns `null` on miss — still nothing like `getClass()`.

```java
Number n = Integer.valueOf(0);

Class<? extends Number> runtime = n.getClass();   // Integer
Class<?> named = Class.forName("java.lang.Number"); // Number, initialized

Class<?> missing = Class.forName("com.example.NoSuch"); // ClassNotFoundException
```

**Listing 1.** `n.getClass()` is `Integer`, not `Number`. `forName("java.lang.Number")` is the named type and runs `<clinit>` if needed. `n.getClass().getName()` is not a substitute for a plugin name you never had.

> [!warning] `getClass()` is not “the declared type”
> It answers *what was allocated*. That is why factories, mocks, and Spring/JDK proxies surprise people who expected the interface’s `Class`.

> [!warning] One-arg `forName` always initializes
> That is the JDBC-driver pattern and the foot-gun. `getClass()` does not take a name and does not look up a loader. `forName("int")` is not `int.class`.

> [!tip] Interview answer
> **`getClass()` is on the instance and gives the live runtime class — subclass, array class, or proxy included.** `Class.forName` is static: you pass a binary name, the one-arg form loads and initializes with the caller’s class loader, and a bad name is checked `ClassNotFoundException`. **Have an object → `getClass()`. Have only a name → `forName`. Have the type in source → `.class`.**
