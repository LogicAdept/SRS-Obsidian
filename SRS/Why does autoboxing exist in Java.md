<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #Java/Versions/5 #SRS

# Why does autoboxing exist in Java?

> [!abstract] Short answer
> Autoboxing exists to **remove the hand-written conversions** between primitives and wrappers once **generics and collections** needed objects. Since Java 5 the compiler inserts `valueOf` / `xxxValue` so `list.add(i)` and `int n = list.get(0)` compile. It is a **compile-time conversion**, not a new JVM type. Primitives stay smaller and non-null; the cost is allocation, GC, and `NullPointerException` on unbox.

## Bridge the two type systems

Java has primitives for arithmetic and wrappers for the object world (`List`, generics, `null`). Before Java 5 you wrote `list.add(Integer.valueOf(i))` and `int n = integer.intValue()` at every boundary. Autoboxing is that same pair of calls, inserted by the compiler ([[In which Java version were autoboxing and unboxing introduced]], [[When does autoboxing occur in Java]]).

That is why the feature shipped with generics: `List<int>` is still illegal; `List<Integer>` plus boxing is the usable API ([[Why cannot Java collections store primitive types]], [[Why are wrapper classes needed in Java]]).

```d2
direction: down
before: "Java 4: write valueOf / intValue" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
after: "Java 5: compiler inserts them" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
before -> after
```

**Fig. 1.** Autoboxing is convenience over the same factories, not a third kind of number.

```java
List<Integer> list = new ArrayList<>();
int i = 5;
list.add(i);                 // add(Integer.valueOf(i))
int n = list.get(0);         // list.get(0).intValue()

// Java 4 style — still what the bytecode does:
list.add(Integer.valueOf(i));
```

**Listing 1.** Conceptual: the feature exists so the first form is legal; the second form is still the mechanism.

The primitive/`Integer` split did not go away. `int` stays 32 bits and cannot be `null`; `Integer` is a heap object ([[How much memory does an Integer object use compared with int]]). Loops that box every `+=` still allocate ([[Is autoboxing always a performance problem in Java]]). Treat Valhalla-style “primitives in generics” as **not** current interview behavior.

> [!warning] It is not a new primitive
> The VM still sees `invokestatic valueOf` and `invokevirtual intValue`. Hidden calls mean hidden NPEs and hidden allocations. Autoboxing made collections pleasant; it did not make `int` an object.

> [!tip] Interview answer
> **Autoboxing exists so you can mix primitives with object APIs — especially `List<Integer>` — without writing `valueOf` and `intValue` everywhere.** The compiler has done that since Java 5. Use `int` for math; accept boxing at collection boundaries; do not pretend `List<int>` works.
