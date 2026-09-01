<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/OOP/Constructors #SRS

# How do you invoke a private constructor using reflection?

> [!abstract] Short answer
> **`getDeclaredConstructor` with the exact parameter `Class` tokens, `setAccessible(true)`, then `newInstance(args)`.** `getConstructor` never sees a private constructor (`NoSuchMethodException`). Without `setAccessible`, `newInstance` throws `IllegalAccessException` while language access control is enforced. That bypass is what private constructors are meant to stop; it is not unlimited.

## Declared lookup, then suppress access checks

Private is an access modifier, not “no constructor.” The reflective lookup must use the **declared** API ([[How can you access constructors using reflection]], [[How would you explain private constructors and common patterns that use them in Java]]). `getDeclaredConstructor()` with no types is the private nullary constructor; `getDeclaredConstructor(String.class)` matches a private `Hidden(String)`.

```d2
direction: down
cls: "Class<T>" {
  width: 150
  height: 40
}
dec: "getDeclaredConstructor(types)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
acc: "setAccessible(true)" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
ni: "newInstance(args)" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
fail: "getConstructor → NoSuchMethodException" {
  width: 320
  height: 50
  style.fill: "#ffebee"
}
cls -> dec
cls -> fail: "public-only"
dec -> acc
acc -> ni
```

**Fig. 1.** Private construction is declared lookup plus `setAccessible`, then the same `newInstance` as a public constructor ([[How can you create an instance of a class using reflection]], [[What does setAccessible do in the Reflection API]]).

```java
class Hidden {
    private Hidden() {}
    private Hidden(String label) {}
}

class Make {
    static Hidden noArg() throws Exception {
        Constructor<Hidden> ctor = Hidden.class.getDeclaredConstructor();
        ctor.setAccessible(true);
        return ctor.newInstance();
    }

    static Hidden labeled(String label) throws Exception {
        Constructor<Hidden> ctor = Hidden.class.getDeclaredConstructor(String.class);
        ctor.setAccessible(true);
        return ctor.newInstance(label);
    }
}
```

**Listing 1.** `getConstructor()` on `Hidden` throws `NoSuchMethodException`. After `setAccessible(true)`, `newInstance` runs the private constructor (unwrap/widen args as usual; constructor throws → `InvocationTargetException`).

Across modules, `setAccessible(true)` still requires the package to be **open** to the caller or it throws `InaccessibleObjectException`. `setAccessible(true)` on a constructor of `java.lang.Class` throws `SecurityException`. An **inner** class still needs the enclosing instance as the first formal parameter. An **abstract** class → `InstantiationException`. An **enum** constructor → `IllegalArgumentException` even after `setAccessible` ([[Can you declare a constructor inside a Java enum]]).

Tests and frameworks use this path because a private constructor is still a constructor. It also means a type that used `private` to enforce a singleton or “utility class” invariant can be allocated again — unless the language already forbids it (enum constants).

> [!warning] `getConstructor` is the wrong method
> It reflects **public** constructors only. A private constructor is not “there but inaccessible” on that API; the lookup fails with `NoSuchMethodException`. Switch to `getDeclaredConstructor` first, then `setAccessible`.

> [!warning] `setAccessible` is not a master key
> It suppresses Java language access checks on that `Constructor` object when the package is open. It does not make enum construction legal, does not instantiate abstracts, and does not skip the enclosing-instance argument for inner classes.

> [!tip] Interview answer
> **`getDeclaredConstructor` for the private signature, `setAccessible(true)`, `newInstance`.** `getConstructor` will not find it. **That can break a singleton that relied on a private constructor — unless the type is an enum, whose constructors refuse `newInstance`.**
