<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #Java/OOP/Constructors #SRS

# How can you access constructors using reflection?

> [!abstract] Short answer
> **Ask `Class` for a `Constructor`, then call `newInstance`.** `getConstructor` / `getConstructors` see only **public** constructors of that class. `getDeclaredConstructor` / `getDeclaredConstructors` see every constructor **declared** on it (any access), including a synthesized default constructor and a record canonical constructor. Lookup matches **exact** `Class` tokens. Non-public construction also needs `setAccessible(true)` ([[What does setAccessible do in the Reflection API]], [[How do you invoke a private constructor using reflection]]).

## Four lookup methods, then `newInstance`

Constructors are not inherited. Unlike `getMethods` / `getFields`, these APIs never return a superclass constructor ([[What is the difference between getMethod and getDeclaredMethod]], [[What is the difference between getField and getDeclaredField]]).

| API | What you get |
| --- | --- |
| `getConstructor(Class<?>…)` | one **public** constructor whose formal types match |
| `getConstructors()` | all **public** constructors of this class |
| `getDeclaredConstructor(Class<?>…)` | one constructor **declared** here, any access |
| `getDeclaredConstructors()` | all constructors declared here (implicit or explicit) |

`getConstructor` / `getDeclaredConstructor` throw `NoSuchMethodException` when there is no match — including when the `Class` is an interface, a primitive, an array type, or `void`. The array forms return a **length-0** array for those same kinds (and `getDeclaredConstructors` is empty for an interface). Neither array is sorted.

`getDeclaredConstructors` includes a default constructor when the class has one, and a record canonical constructor when the type is a record ([[How would you explain the default constructor synthesized by the Java compiler]], [[What is a canonical constructor in a Java record]]).

```d2
direction: down
cls: "Class<?> c" {
  width: 160
  height: 50
}
pub: "getConstructor(types)\ngetConstructors()" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
dec: "getDeclaredConstructor(types)\ngetDeclaredConstructors()" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ctor: "Constructor<T>" {
  width: 200
  height: 50
}
ni: "newInstance(args)" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
cls -> pub: "public only"
cls -> dec: "declared, any access"
pub -> ctor
dec -> ctor
ctor -> ni
```

**Fig. 1.** Lookup on `Class`, then construct. Private / package / protected still need `setAccessible` before `newInstance` succeeds.

```java
class Holder {
    public Holder() {}
    public Holder(String label) {}
    private Holder(int n) {}
}

class Demo {
    static Holder noArg(Class<Holder> type) throws Exception {
        Constructor<Holder> ctor = type.getConstructor();
        return ctor.newInstance(); // zero-arg: empty array or null is also legal
    }

    static Holder labeled(Class<Holder> type, String label) throws Exception {
        Constructor<Holder> ctor = type.getConstructor(String.class);
        return ctor.newInstance(label);
    }

    static Constructor<?>[] declared(Class<Holder> type) {
        return type.getDeclaredConstructors();
    }
}
```

**Listing 1.** Public constructors via `getConstructor` plus `newInstance`. `declared` also contains the private `Holder(int)` that `getConstructor(int.class)` would not find.

`Constructor.getParameterTypes()` returns those formal types in declaration order (length 0 if none) — the same tokens you pass to `getConstructor` / `getDeclaredConstructor`. `getParameterCount()` counts formal parameters, including implicit ones.

`newInstance` unwraps wrappers to primitives and allows **widening** conversions; a **narrowing** conversion throws `IllegalArgumentException`. Lookup does **not** widen: `getConstructor(Integer.class)` does not find `Holder(int)`.

That is also the reflective way to **construct** once you have the `Constructor` ([[How can you create an instance of a class using reflection]]).

## Non-public constructors and extra parameters

For a non-public constructor: `getDeclaredConstructor`, then `setAccessible(true)`, then `newInstance` ([[How do you invoke a private constructor using reflection]], [[How would you explain private constructors and common patterns that use them in Java]]). Without `setAccessible`, `newInstance` throws `IllegalAccessException` while language access control is enforced. Across modules, `setAccessible` still requires the package to be **open** or it throws `InaccessibleObjectException`. `setAccessible(true)` on a constructor of `java.lang.Class` itself throws `SecurityException`.

If the type is an **inner class** in a non-static context, the formal parameter list **starts with the enclosing instance**. You must pass that `Class` token on lookup and that instance as the first `newInstance` argument.

```java
class Outer {
    class Inner {
        private Inner(String label) {}
    }
}

class Nested {
    static Outer.Inner make(Outer outer, String label) throws Exception {
        Constructor<Outer.Inner> ctor =
                Outer.Inner.class.getDeclaredConstructor(Outer.class, String.class);
        ctor.setAccessible(true);
        return ctor.newInstance(outer, label);
    }
}
```

**Listing 2.** Enclosing instance is parameter 0 for both lookup and `newInstance`. Compact record constructors can also expose implicit parameters on `getParameterTypes()`.

`newInstance` initializes the declaring class if needed. If the constructor body throws, that throwable is wrapped in `InvocationTargetException`. An **abstract** declaring class → `InstantiationException`. An **enum** constructor → `IllegalArgumentException` even after `setAccessible` ([[Can you declare a constructor inside a Java enum]]).

> [!warning] `getConstructor` is not “any constructor”
> It is public-only, this class only. A private constructor is a `NoSuchMethodException` until you switch to `getDeclaredConstructor`. `getConstructors()` has the same public filter; it does not list `super` constructors.

> [!warning] Exact types at lookup, conversions only at `newInstance`
> `int.class` and `Integer.class` are different constructors. Inner-class and some record compact constructors have extra formal parameters that do not appear in the Java source list you might quote from memory.

> [!tip] Interview answer
> **`getConstructor` / `getConstructors` for public constructors of that class; `getDeclaredConstructor` / `getDeclaredConstructors` for every constructor it actually declares.** Then `newInstance` with arguments that match those `Class` tokens — `setAccessible(true)` if the constructor is not accessible. Remember the enclosing-instance parameter on inner classes, and that enum constructors refuse `newInstance`.
