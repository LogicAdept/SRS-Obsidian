<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# When does autoboxing occur in Java?

> [!abstract] Short answer
> Autoboxing runs when a **primitive is used where its matching wrapper is required**: **assignment** (`Integer j = a`, `return 5`, array initializers), **invocation** (`list.add(25)`, a method parameter of type `Integer`), and **casts** (`(Integer) 5`). The compiler inserts `valueOf` ([[What method does the compiler insert when autoboxing an int]]). It does **not** “widen then box” (`Long n = 1` is illegal). Unboxing is the reverse contexts, via `xxxValue`.

## Contexts that box

Boxing conversion is applied in assignment, method/constructor invocation, and casting. Typical interview list:

1. **Assignment** — `Integer j = a;`, fields, `return` of a primitive from a wrapper-returning method, `Integer[] xs = { 1, 2 }`.
2. **Invocation** — `void f(Integer n)`, `list.add(25)` ([[How does adding an int to an ArrayList of Integer autobox]]).
3. **Cast** — `(Integer) 5` / `(Object) 5` (box then widen the reference).

Compound assignment and `++` on an `Integer` variable also box the result they store.

```d2
direction: down
prim: "int 25" {
  width: 120
  height: 40
}
assign: "Integer j = 25" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
invoke: "list.add(25)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
cast: "(Integer) 25" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
prim -> assign
prim -> invoke
prim -> cast
```

**Fig. 1.** Same boxing conversion; three contexts that request a wrapper.

```java
int a = 25;
Integer j = a;                   // assignment boxing
List<Integer> list = new ArrayList<>();
list.add(25);                    // invocation boxing
Integer c = (Integer) 25;        // cast boxing

Integer ret() { return a; }      // return is an assignment context
```

**Listing 1.** Conceptual: the three places the compiler inserts `Integer.valueOf`.

Unboxing fires in the mirror cases: `int x = j`, arithmetic, comparisons, `++` / `+=`, numeric `? :` when the type is primitive ([[What method does the compiler insert when unboxing an Integer]]). `null` there is `NullPointerException`.

This has been in the language since Java 5 ([[In which Java version were autoboxing and unboxing introduced]]).

> [!warning] Matching wrapper only — not “any number type”
> A `byte` **variable** does not box to `Short` or `Integer`. `Long n = 1;` does not compile (`int` does not widen-then-box). Constant `int`s may narrow-then-box into `Byte`/`Short`/`Character` on **assignment**, not as method arguments ([[What are the autoboxing rules when assigning a primitive to a wrapper]]).

> [!tip] Interview answer
> **Autoboxing happens when a primitive is assigned, passed, or cast to its wrapper — `Integer j = 5`, `list.add(5)`, `(Integer) 5`.** The compiler calls `valueOf`. Unboxing is the opposite, with `intValue()`, and `null` throws. It will not turn `1` into a `Long`.
