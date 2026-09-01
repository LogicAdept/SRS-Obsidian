<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What method does the compiler insert when unboxing an `Integer`?

> [!abstract] Short answer
> **`Integer.intValue()`.** `int x = someInteger` is compiled as `someInteger.intValue()`. If the reference is `null`, that call throws `NullPointerException` — the source looks like an assignment, the NPE is a method invocation. Autoboxing’s pair is `Integer.valueOf(int)` ([[What method does the compiler insert when autoboxing an int]]).

## Unboxing is `intValue()`

Unboxing conversion of an `Integer` *is* `r.intValue()`. The same insertion happens anywhere an `Integer` is used as an `int`: assignment, arithmetic, `++` / `+=`, comparison, and a numeric `? :` arm ([[How do you convert a wrapper to a primitive with xxxValue methods]], [[What happens when a ternary operator unboxes a null Integer in Java]]).

```d2
direction: down
src: "Integer obj\nint x = obj" {
  width: 220
  height: 50
}
call: "obj.intValue()" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
out: "int" {
  width: 100
  height: 40
  style.fill: "#e8f5e9"
}
npe: "obj == null → NPE" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
src -> call -> out
call -> npe
```

**Fig. 1.** Unboxing is `invokevirtual Integer.intValue`; `null` fails at that call.

```java
Integer obj = Integer.valueOf(42);
int x = obj;                     // obj.intValue()

Integer missing = null;
// int boom = missing;           // NullPointerException: intValue() on null

Map<String, Integer> counts = new HashMap<>();
// int n = counts.get("absent"); // get returns null → same NPE
```

**Listing 1.** Conceptual: assignment unbox, and the `Map.get` trap.

The other wrappers unbox through their matching `xxxValue` methods: `booleanValue`, `byteValue`, `shortValue`, `charValue`, `longValue`, `floatValue`, `doubleValue`. `Number` also offers cross-type conversions (`doubleValue` on an `Integer`); those are not the unboxing conversion, which always matches the wrapper’s primitive.

A field `Integer n;` defaults to `null`, so `int x = n;` throws. A local `Integer` has no default and will not compile until assigned ([[What default values do wrapper-typed fields receive in Java]]).

> [!warning] The NPE is the hidden `intValue()`, not a “failed assignment”
> `int x = obj;` with `obj == null` does not leave `x` as `0`. Evaluation of `intValue()` throws and the assignment never happens. Helpful NPEs (Java 14+) can name that `intValue()` call ([[What did Java 14 change about NullPointerException messages]]).

> [!tip] Interview answer
> **Unboxing an `Integer` inserts `intValue()`.** That is a real virtual call, so a `null` wrapper is `NullPointerException` even in `int x = obj` or `sum += map.get(key)`. Boxing is `valueOf`; unboxing is `intValue()`.
