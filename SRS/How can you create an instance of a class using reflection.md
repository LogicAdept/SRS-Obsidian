<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #Java/OOP/Constructors #Java/Versions/9 #SRS

# How can you create an instance of a class using reflection?

> [!abstract] Short answer
> **Obtain a `Constructor` and call `newInstance` with matching arguments.** The Java SE 9 replacement for the deprecated `Class.newInstance()` is `clazz.getDeclaredConstructor().newInstance()` for a nullary constructor. That wraps constructor failures in `InvocationTargetException` instead of letting checked exceptions leak. Parameterized construction is `getConstructor` / `getDeclaredConstructor` plus `newInstance(args)`. Arrays are `Array.newInstance`, not `Class.newInstance`.

## `Constructor.newInstance` is the reflective `new`

You need a `Class` first ([[How can you get the Class object in Java]], [[What does Class.forName do and what are its overloads]]), then a constructor ([[How can you access constructors using reflection]]). `newInstance` initializes the declaring class if needed, unwraps wrappers to primitives, and allows widening (not narrowing).

```d2
direction: down
cls: "Class<T>" {
  width: 160
  height: 45
}
ctor: "getDeclaredConstructor(types)\nor getConstructor(types)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ni: "Constructor.newInstance(args)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
old: "Class.newInstance()\ndeprecated since 9" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
arr: "Array.newInstance(component, length)" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
cls -> ctor
ctor -> ni
cls -> old: "nullary only"
cls -> arr: "array Class"
```

**Fig. 1.** Ordinary types go through `Constructor.newInstance`. `Class.newInstance` is the old nullary shortcut. Array types use `java.lang.reflect.Array`.

```java
class Holder {
    public Holder() {}
    public Holder(String label) {}
}

class Create {
    static Holder noArg(Class<Holder> type) throws Exception {
        return type.getDeclaredConstructor().newInstance();
    }

    static Holder labeled(Class<Holder> type, String label) throws Exception {
        return type.getConstructor(String.class).newInstance(label);
    }
}
```

**Listing 1.** Documented nullary replacement (`getDeclaredConstructor().newInstance`) and a public parameterized constructor. Lookup uses exact `Class` tokens (`String.class`, not a superclass).

`Class.newInstance()` is `@Deprecated(since = "9")`. It behaves like `new` with an **empty** argument list: only the **nullary** constructor, and it **propagates** whatever that constructor throws — including a **checked** exception — so the compiler’s `throws` checking is bypassed. `Constructor.newInstance` wraps that throwable in checked `InvocationTargetException`. The extra types you must handle on the replacement (`InvocationTargetException`, `NoSuchMethodException`) are both `ReflectiveOperationException`.

A non-public constructor still needs `getDeclaredConstructor` and `setAccessible(true)` before `newInstance` ([[How do you invoke a private constructor using reflection]], [[What does setAccessible do in the Reflection API]]). `getConstructor()` does not see it.

```java
String[] names = (String[]) Array.newInstance(String.class, 3);
int[][] grid = (int[][]) Array.newInstance(int.class, 2, 4);
```

**Listing 2.** `Class.newInstance` cannot allocate an array (`InstantiationException`). `Array.newInstance` takes a component type plus length, or `int...` dimensions (total rank ≤ 255).

## What refuses to construct

`Class.newInstance` throws `InstantiationException` when the `Class` is abstract, an interface, an array, a primitive, `void`, or has **no nullary constructor** ([[Can a Java interface declare a constructor]], [[How would you explain the default constructor synthesized by the Java compiler]], [[How can you determine if a Class represents an array]]). `IllegalAccessException` if the class or that nullary constructor is not accessible. `Constructor.newInstance` throws `InstantiationException` for an **abstract** declaring class, `IllegalArgumentException` for an **enum** constructor, and `InvocationTargetException` when the constructor body throws.

Inner classes in a non-static context need the enclosing instance as the first argument ([[How can you access constructors using reflection]]).

> [!warning] `getConstructor()` is not the documented replacement
> The JavaDoc replacement is `getDeclaredConstructor().newInstance()`, which finds a **declared** nullary constructor of any access. `getConstructor()` is public-only. After the replacement, a **private** nullary constructor still throws `IllegalAccessException` until `setAccessible(true)`.

> [!warning] `Class.newInstance` lies about checked exceptions
> A constructor `throws IOException` becomes a checked `IOException` at the `Class.newInstance()` call site with no `InvocationTargetException` wrapper. That is why it was deprecated in 9. Always unwrap `getCause()` / `getTargetException()` on `Constructor.newInstance` instead of assuming the constructor “doesn’t throw.”

> [!tip] Interview answer
> **Call `Constructor.newInstance` after `getConstructor` or `getDeclaredConstructor` — that is reflective `new`, including constructors with parameters.** Replace `Class.newInstance()` with `getDeclaredConstructor().newInstance()`; it was deprecated in Java 9 because constructor checked exceptions used to leak. **Arrays are `Array.newInstance`; abstract types, interfaces, and a missing no-arg constructor fail with `InstantiationException`.**
