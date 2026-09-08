<!--
reps: 0
priority: 0
-->
#Java/Language #SRS

# What is the instanceof operator for in Java?

> [!abstract] Short answer
> `instanceof` asks whether a **reference** (or `null`) matches a type or a pattern, and yields `boolean`. In the **type-comparison** form `e instanceof T`, the result is whether `e` could be cast to `T` without `ClassCastException`. In the **pattern** form `e instanceof String s` (standard from **Java 16**), a `true` result also **initializes** the pattern variable. `null` is `false` in both forms — never a match, never a bound variable.

## Two operators that share one keyword

```d2
direction: down
e: "left operand\nreference or null type" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
cmp: "e instanceof T\ntrue iff a cast to T would succeed" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
pat: "e instanceof String s\nmatch + initialize s" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
nil: "null -> false\nno pattern variable" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
e -> cmp
e -> pat
cmp -> nil
pat -> nil
```

**Fig. 1.** Same keyword. Type comparison tests a cast. A pattern also binds a local when the test succeeds.

The left operand must be a **reference type or the null type**; `3 instanceof Integer` is a compile error. For type comparison, `e` must be **checked-cast compatible** with `T` — if no possible non-null value of `e`’s static type can be a `T`, the expression does not compile (same reason the cast would be rejected). At run time, a non-null value is `true` exactly when that cast would not throw `ClassCastException`.

The pattern form requires the pattern to be **applicable** at the static type of `e`. On a `true` result, every pattern variable in that pattern is initialized and in scope where the match is guaranteed — typically the true branch of `if`, or the remainder of a `&&` chain. That local is a pattern variable, not a field ([[How would you explain kinds of variables in Java such as local and instance]]). `null` still yields `false`, so `s` is not assigned.

From Java 16 the type on the right of a **type comparison** no longer has to be reifiable: `x instanceof ArrayList<Integer>` can be legal when there is a casting conversion from `x`’s type. `List<Integer> x instanceof ArrayList<String>` is still a compile error — erasure does not make unrelated parameterizations cast-compatible. Pattern matching for `instanceof` is the same release; it is not a Java 14 production feature (14/15 were preview).

```java
class Point { int x, y; }
class Element { int atomicNumber; }
record Pair(int x, int y) {}

class Demo {
    static String label(Object o) {
        if (o instanceof String s && s.length() > 3) {
            return s;
        }
        if (o instanceof Point) {
            return "point";
        }
        return "other";
    }

    static int sumIfPair(Object p) {
        if (p instanceof Pair(int x, int y)) { // record pattern, Java 21
            return x + y;
        }
        return 0;
    }
}

// Element e = new Element();
// boolean b = e instanceof Point;   // compile error: types are disjoint
// boolean p = 1 instanceof Integer; // compile error: left is primitive
```

**Listing 1.** Pattern `instanceof` binds `s` only when the test is true. Classic `instanceof Point` is a type comparison and still needs a cast if you want a `Point`. The record pattern on `Pair` is Java 21. Disjoint types and primitives do not compile.

A **record pattern** in `instanceof` (`p instanceof Point(int x, int y)`) is the Java 21 deconstruction form, the same idea as `case Point(int x, int y)` ([[How do records work with pattern matching in switch]]). Type patterns in `switch` are a different host: pattern `switch` is final in **21**; `instanceof` patterns were already final in **16** ([[What is the difference between pattern matching and a switch statement]], [[How would you explain Java 17 21]]). Sealed types make some `instanceof` / cast pairs provably disjoint ([[How would you explain Sealed classes]]).

> [!warning] `null instanceof T` is `false`, not an NPE
> People expect a null check to throw. Both forms return `false`. There is no pattern variable to use after a failed match. Do not write `if (x != null && x instanceof String)` as if the first test were required for safety — `instanceof` already rejects `null`.

> [!warning] A compile-time impossible test is an error, not `false`
> `element instanceof Point` when `Element` and `Point` cannot share an instance does not compile. That is the same rule as a doomed cast. From 16 you *can* test some parameterized types, but `List<Integer>` versus `ArrayList<String>` is still rejected. Pattern `instanceof` does not replace `equals`; it is a type test plus a binding.

> [!tip] Interview answer
> **`instanceof` is a boolean type test: `null` is false, and a non-null value is true when a cast to that type would succeed.** From Java 16 you can write `o instanceof String s` and use `s` without a second cast. Pattern `switch` is a later, separate feature (final in 21); `instanceof` itself never switched on values.
