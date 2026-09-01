<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #SRS

# How can you invoke a method using reflection?

> [!abstract] Short answer
> **Look up a `Method` on `Class`, then call `invoke(obj, args…)`.** `getMethod(name, parameterTypes)` finds a **public** method (including inherited). `getDeclaredMethod` finds a method **declared** on that class, any access. `invoke` takes the receiver (`null` is legal for a **static** method), unwraps/widens arguments, and returns a wrapped result — or `null` if the method is `void`. Exceptions thrown by the target are wrapped in `InvocationTargetException`.

## Lookup, then `invoke`

The name and parameter `Class` tokens must match **exactly** at lookup (`int.class` is not `Integer.class`). `getMethod` / `getDeclaredMethod` throw `NoSuchMethodException` if there is no match. They do not return constructors or the class initializer — those are not methods you `invoke` ([[What is the difference between getMethod and getDeclaredMethod]], [[How do you invoke overloaded methods using reflection]], [[How can you access constructors using reflection]]).

```d2
direction: down
cls: "Class<?> c" {
  width: 160
  height: 45
}
pub: "getMethod(name, types)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
dec: "getDeclaredMethod(name, types)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
m: "Method" {
  width: 140
  height: 40
}
inv: "invoke(obj, args…)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
cls -> pub: "public, inherited OK"
cls -> dec: "declared here, any access"
pub -> m
dec -> m
m -> inv
```

**Fig. 1.** Obtain a `Method`, then dispatch. Private / package / protected still need `setAccessible(true)` before `invoke` succeeds ([[What does setAccessible do in the Reflection API]]).

```java
class Target {
    public String greet(String name) {
        return "hi " + name;
    }

    public static int answer() {
        return 42;
    }

    private void hidden() {}
}

class Call {
    static Object greet(Target t) throws Exception {
        Method m = Target.class.getMethod("greet", String.class);
        return m.invoke(t, "Ada");
    }

    static Object answer() throws Exception {
        Method m = Target.class.getMethod("answer");
        return m.invoke(null); // static: receiver is ignored
    }

    static void hidden(Target t) throws Exception {
        Method m = Target.class.getDeclaredMethod("hidden");
        m.setAccessible(true);
        m.invoke(t);
    }
}
```

**Listing 1.** Public instance, public static (`null` receiver), and private (`getDeclaredMethod` + `setAccessible`). Zero-arg `invoke` may pass an empty array or `null` for `args`.

`Method.invoke` unwraps wrappers to primitives and allows **widening**; a **narrowing** conversion throws `IllegalArgumentException`. For an **instance** method it uses **dynamic lookup** (JLS 15.12.4.4): the runtime type of `obj` can override. For a **static** method, `obj` is ignored (may be `null`) and the declaring class is initialized if needed. A primitive return is wrapped; a primitive **array** return is not element-wrapped; `void` returns `null`.

Wrong receiver type or arity → `IllegalArgumentException`. Instance method with `obj == null` → `NullPointerException`. Inaccessible method while access checks are on → `IllegalAccessException`. Failed `<clinit>` → `ExceptionInInitializerError`. Static methods are the same “`null` receiver” pattern as static fields ([[How do you access static fields using reflection]]).

> [!warning] The method’s `throws` is not what `invoke` throws
> If `greet` throws `IOException`, `invoke` throws **`InvocationTargetException`** whose cause is that `IOException`. Catch `InvocationTargetException` and unwrap `getCause()` / `getTargetException()`. Do not expect the checked type on the `invoke` call site.

> [!warning] `getMethod` is public-only and virtual
> A private method is `NoSuchMethodException` until you switch to `getDeclaredMethod`. A `Method` taken from a superclass still **dispatches to the override** on the instance — you did not “call the super body” by reflecting the super `Method`.

> [!tip] Interview answer
> **`getMethod` or `getDeclaredMethod` with the exact name and `Class` parameter tokens, then `invoke(receiver, args)`.** Static methods take `null` as the receiver; private methods need `getDeclaredMethod` and `setAccessible(true)`. **Whatever the target throws is wrapped in `InvocationTargetException` — `void` comes back as `null`.**
