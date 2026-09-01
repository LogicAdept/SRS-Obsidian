<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# How do you iterate over all Java enum constants?

> [!abstract] Short answer
> Call the enum’s implicit `public static E[] values()` and use an enhanced `for`. The array is the constants in **declaration order**. `values()` is generated on the enum type; it is not a method of `java.lang.Enum` or `Object`. `EnumSet.allOf(E.class)` is the same universe as a set ([[What is EnumSet]]).

## `values()` is the language API

Each enum class `E` has an implicitly declared `values()`. That is the operation the language uses to walk every constant. The usual loop is exactly the spec’s example:

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    void printAll() {
        for (Day d : Day.values()) {
            System.out.println(d);
        }
    }
}
```

**Listing 1.** Enhanced `for` over `values()`. Prints `MON` … `SUN` in source order. `valueOf` is the inverse lookup ([[How do you convert a String to a Java enum]]).

```d2
direction: down
v: "Day.values()\n[MON, TUE, …, SUN]" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
loop: "for (Day d : …)" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
set: "EnumSet.allOf(Day.class)" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}

v -> loop
v -> set
```

**Fig. 1.** One universe of constants. The array is for looping; `EnumSet` is for set algebra on that same universe.

`values()` is **not** inherited because you extend `Enum`. Dumps that say that are mixing it up with `name()` / `ordinal()` / `compareTo` ([[Can a Java enum extend a class]]). You cannot write your own `values()`; it would clash with the implicit method.

When you only have a `Class` token, `Class.getEnumConstants()` returns the constants or `null` if the class is not an enum. In JDK 21 that public method clones a cached array obtained by invoking `values()` once — useful from reflective code, not the everyday loop.

## Other loops on the same set

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Walk {
    void asSet() {
        for (Day d : java.util.EnumSet.allOf(Day.class)) {
            System.out.println(d);
        }
    }
}
```

**Listing 2.** `allOf` is every constant, still in declaration order. Use it when you want an `EnumSet` (union, complement), not when you only need to print.

An empty enum has `values().length == 0` ([[How do you create a Java enum with no instances]]). You cannot grow the array to invent constants ([[Can you add constants to a Java enum at runtime]]). Treat the returned array as a snapshot: the language does not define what happens if you write into it; do not.

> [!warning] `values()` is not on `Enum`
> `Day.values()` compiles. `Enum.values()` does not. Lists that put `values()` next to `name()` as “inherited from `Enum`” are wrong about `values()` (and about `valueOf(String)`).

> [!warning] Do not write `for (int i = 0; i < Day.values().length; i++)`
> The enhanced-`for` form evaluates `values()` once. An indexed loop that calls `values()` in the bound and again in the body repeats the call. Prefer `Day[] all = Day.values();` if you need indexes.

> [!tip] Interview answer
> **`for (E e : E.values())` — `values()` is generated on the enum and returns the constants in declaration order.** It is not inherited from `Enum`. `EnumSet.allOf` is the same set when you need set operations. `valueOf(String)` is lookup by name, not iteration.
