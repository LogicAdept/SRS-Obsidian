<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can you override `compareTo` on a Java enum?

> [!abstract] Short answer
> **No.** `Enum.compareTo` is `final`. The natural order of an enum is the order the constants are declared — the same ranking `ordinal()` exposes ([[What does ordinal do on a Java enum]]). An enum declaration cannot override any `final` method of `Enum`. For a different order, supply a `Comparator`; do not try to redefine `compareTo`.

## Why it is locked

`java.lang.Enum` implements `Comparable<E>`. Its `compareTo` is `final` and compares constants of **the same enum type** only. The documented order is declaration order. That is also why `enum Color implements Comparable<String>` is illegal, and restating `implements Comparable<Color>` does not give you a hook ([[Can a Java enum implement an interface]]).

`equals`, `hashCode`, `clone`, `name`, and `ordinal` are `final` too. You cannot make `compareTo` agree with a custom `equals` because you cannot write either ([[What is the difference between comparing enums with == and equals]]).

```d2
direction: down
decl: "enum Size { S, M, L }" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
nat: "compareTo / ordinal\ndeclaration order (final)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
cmp: "new TreeSet<>(comparator)\ncustom order" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

decl -> nat
decl -> cmp
```

**Fig. 1.** Natural order is baked into `Enum`. A `Comparator` is a separate ordering used by sorts and sorted collections.

```java
enum Size { S, M, L, XL }

// int compareTo(Size other) { return name().compareTo(other.name()); }
// compile error: cannot override final method from Enum
```

**Listing 1.** Conceptual: any `compareTo` in the enum body conflicts with the `final` method inherited from `Enum`.

`S.compareTo(M)` is negative, `L.compareTo(S)` is positive, `M.compareTo(M)` is zero — the same comparisons as `Integer.compare(ordinal(), other.ordinal())` ([[What is the difference between ordinal and compareTo on a Java enum]]). Distinct enum types do not compile against each other’s `compareTo` (`E` is the enum type parameter).

## Different order: `Comparator`, not an override

Sorted collections use natural order unless you pass a comparator. `TreeSet` is ordered by `Comparable.compareTo` **or** by a `Comparator` given to the constructor ([[Can you use a Java enum with TreeSet or TreeMap]]).

```java
enum Size { S, M, L, XL }

java.util.TreeSet<Size> byDeclaration = new java.util.TreeSet<>();
byDeclaration.add(Size.L);
byDeclaration.add(Size.S);
// iteration: S, L — declaration order

java.util.TreeSet<Size> byName = new java.util.TreeSet<>(
        (a, b) -> a.name().compareTo(b.name()));
byName.add(Size.L);
byName.add(Size.S);
// iteration: L, S — alphabetical on the constant name
```

**Listing 2.** Same constants, two orders. `byName` never overrides `compareTo`; `Size.compareTo` still follows `S < M < L < XL`.

> [!warning] Inserting a constant in the middle changes `compareTo` for everyone
> Reordering or inserting constants is a binary-compatible source change, but it shifts `ordinal` and therefore natural order. Do not persist `ordinal` or “position in the enum” as a business key if the list can grow. Put a stable field on the constant if the order is data, not source layout.

> [!warning] A custom `Comparator` is not `compareTo`
> `new TreeSet<>(comparator)` and `List.sort(comparator)` change how **that** collection or call sorts. `size.compareTo(other)`, `TreeSet` with no comparator, and `EnumSet` iteration still use declaration order. Interviewers who ask “can you override `compareTo`” want **no**, then the comparator workaround.

> [!tip] Interview answer
> **No — `compareTo` is `final` on `Enum`, and the order is the declaration order of the constants.** That is the same ranking as `ordinal`. If you need another order, pass a `Comparator` into `sort` or `TreeSet`; do not try to override `compareTo` on the enum.
