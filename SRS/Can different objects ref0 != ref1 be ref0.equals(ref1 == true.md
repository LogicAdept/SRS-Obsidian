<!--
reps: 0
priority: 0
-->
#Java/Language #Java/HashCodeEquals #SRS

# Can distinct references still be equal under `equals`?

> [!abstract] Short answer
> **Yes.** `ref0 != ref1` only means two different objects. If their class defines **value** `equals`, `ref0.equals(ref1)` can still be `true`. With the inherited `Object.equals`, that never happens: it returns `true` if and only if `ref0 == ref1`.

## Identity vs value equality

`==` on references compares object identity. `equals` may mean the same thing or a logical equivalence the class chooses. [[How would you explain the Object equals method contract]] is the five-clause contract that any override must keep.

```d2
direction: down
refs: "ref0 != ref1\n(two instances)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
objectEq: "Object.equals\n→ false (identity only)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
valueEq: "Overridden equals\n→ may be true" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

refs -> objectEq
refs -> valueEq
```

**Fig. 1.** Distinct references always fail `==`. They fail default `equals` too, but not necessarily a value `equals`.

OpenJDK’s default is identity:

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

**Listing 1.** Conceptual `Object.equals` (OpenJDK): `true` only for the same instance.

So for a class that does **not** override `equals`, `ref0 != ref1` already implies `ref0.equals(ref1) == false`.

## When distinct instances compare equal

Any class with value semantics can make two instances equivalent: `String`, boxed numbers, `record` types, your own final value class, and so on. You do not always write the override yourself — many library types already provide one.

```java
String ref0 = new String("hi");
String ref1 = new String("hi");

System.out.println(ref0 != ref1);       // true
System.out.println(ref0.equals(ref1));  // true
```

**Listing 2.** Java 8+: two distinct `String` instances, same content. Prefer string literals in real code; `new String(...)` is only to force two objects.

```java
record UserId(long value) {}

UserId a = new UserId(42);
UserId b = new UserId(42);

System.out.println(a != b);      // true
System.out.println(a.equals(b)); // true
```

**Listing 3.** Java 16+: a `record` generates component-based `equals` (and a matching `hashCode`).

When you override `equals` for hash-based collections, override `hashCode` from the same fields. See [[Why should equals and hashCode be overridden together]] and [[How would you explain the equals and hashCode contract together in Java]].

> [!warning] Arrays keep identity `equals`
> Two `int[]` or `Object[]` with the same elements still use `Object`’s identity `equals`. Content comparison is `Arrays.equals` / `Arrays.deepEquals`, not `a.equals(b)`.

> [!warning] Overload is not an override
> `equals(MyType)` without `equals(Object)` does not replace `Object.equals`. Collections still call `equals(Object)`, so distinct equal-looking instances stay unequal for `HashSet` / `HashMap`. [[How do you override equals correctly in Java]] covers that trap.

> [!tip] Interview answer
> **Yes — if the runtime class uses value equality.** Default `Object.equals` is the same as `==`, so distinct references are never equal under it. Types like `String`, records, or a correct custom override can make `ref0.equals(ref1)` true while `ref0 != ref1`. Remember to keep `hashCode` in sync when you override `equals`.
