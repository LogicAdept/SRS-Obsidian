<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS

# How do you invoke overloaded methods using reflection?

> [!abstract] Short answer
> **Pick the overload at lookup time with an exact `Class[]` of formal parameter types, then `invoke`.** `getMethod` / `getDeclaredMethod` take the shared name plus those types in declaration order. There is no compile-time overload resolution: a wrong `Class` token is `NoSuchMethodException`, not “the other `print`.” `invoke` only unwraps and **widens** arguments for the `Method` you already obtained.

## Signature in, then `invoke`

Language overloads share a name and differ by parameter types. Reflection identifies a method the same way the `Class` APIs are specified: **simple name** + **formal parameter types in declared order**. `parameterTypes == null` is treated as an empty array (the no-arg overload). Constructors use the same token list on `getConstructor` / `getDeclaredConstructor` ([[How can you invoke a method using reflection]], [[What is the difference between getMethod and getDeclaredMethod]], [[How can you access constructors using reflection]]).

```d2
direction: down
name: "name + Class[] formals" {
  width: 240
  height: 50
}
lookup: "getMethod / getDeclaredMethod" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
hit: "one Method" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
miss: "NoSuchMethodException" {
  width: 240
  height: 45
  style.fill: "#ffebee"
}
inv: "invoke(obj, args…)\nwiden / unwrap only" {
  width: 260
  height: 60
}
name -> lookup
lookup -> hit: "exact match"
lookup -> miss: "no such formals"
hit -> inv
```

**Fig. 1.** Choose the overload with `Class` tokens. `invoke` does not re-run javac overload resolution.

```java
class Printer {
    public void print(int n) {}
    public void print(String s) {}
    public void print(Object o) {}
}

class Call {
    static void asInt(Printer p) throws Exception {
        Method m = Printer.class.getMethod("print", int.class);
        m.invoke(p, 3); // Integer 3 unwraps to int
    }

    static void asString(Printer p) throws Exception {
        Method m = Printer.class.getMethod("print", String.class);
        m.invoke(p, "x");
    }
}
```

**Listing 1.** Three overloads of `print`. `getMethod("print", Integer.class)` does **not** find `print(int)` — lookup is exact, not boxing. `getMethod("print", Object.class)` finds `print(Object)` even if you later `invoke` with a `String`; it will not switch to `print(String)`.

`getDeclaredMethod` is the same token rule for a method **declared** on that class (any access). If the JVM has two declared methods with the same name and parameter types but different return types (covariant override + bridge), `getDeclaredMethod` returns the one with the more specific return type. That is not language overloading (the language forbids two methods that differ only by return type).

Varargs: the last formal is an array type. Look up `foo(String...)` as `getMethod("foo", String[].class)`, then pass a `String[]` (or let `invoke` apply method-invocation conversion to that array parameter). `Method.isVarArgs()` reports the declaration.

> [!warning] Wrong `Class[]` is not “pick another overload”
> `NoSuchMethodException` means no method with that name **and those exact formals** (or you used `getMethod` on a non-public overload). Reflection will not choose `print(Object)` because `print(String)` failed.

> [!warning] `int.class` and `Integer.class` are different overloads
> Compile-time calls box and apply most-specific overload choice. `getMethod` does neither. After you have the `Method`, `invoke` still **refuses narrowing** (`IllegalArgumentException`) and will not re-select a sibling overload.

> [!tip] Interview answer
> **Name plus `Class` tokens for the formal parameters — that is how you name an overload to reflection.** Then `invoke` on that `Method`. **A mismatch is `NoSuchMethodException`; `int` vs `Integer` is a mismatch.** `invoke` only converts arguments for the method you already picked.
