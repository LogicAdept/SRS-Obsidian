<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Implementation #SRS

# What is the difference between `getClass()` and `instanceof` in `equals`?

> [!abstract] Short answer
> **`instanceof` allows a subclass (or interface implementor); `getClass() ==` demands the same runtime class.** `instanceof` is also `false` for `null`. Neither is mandated by `Object.equals`. `instanceof` plus extra subclass fields can **break symmetry**. Exact `getClass()` keeps symmetry by refusing subclasses. JDK lists/sets equal any other list/set; records require the **same record class**.

## Two type tests

`that instanceof MyClass` is true when `that` could be cast to `MyClass` without `ClassCastException` — this class, a subclass, or an implementor of that interface. `null instanceof MyClass` is **false** (no NPE).

`this.getClass() == that.getClass()` compares the two **runtime** `Class` objects. A subclass has a different `Class`, so it fails. `that` must be non-null first or `that.getClass()` throws. [[How would you explain someObj.equals(null)]] [[What is the Object equals contract]]

```text
that == null
  instanceof MyClass          false
  that.getClass()             NPE

that is MyClass
  both                        true

that is SubMyClass
  instanceof MyClass          true
  getClass() ==               false
```

**Listing 1.** Null and subclass are the forks. [[How do you override equals correctly in Java]]

The dump’s “always use `getClass()` for a correct contract” is **too strong**. `Object.equals` requires an equivalence relation (reflexive, **symmetric**, transitive). Both tests can satisfy that if you do not mix them across a hierarchy.

```d2
direction: down
arg: "equals(Object that)" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
io: "instanceof MyClass\nsubtypes OK, null false" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
gc: "getClass() ==\nexact class only" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

arg -> io
arg -> gc
```

**Fig. 1.** Same goal (reject the wrong type); different subtype policy.

```java
class Point {
    int x, y;
    // instanceof Point — a ColoredPoint is a Point
}

class ColoredPoint extends Point {
    String color;
    // instanceof ColoredPoint — a plain Point is not
}

Point p = new Point();          // x,y only
ColoredPoint c = new ColoredPoint();

p.equals(c); // true if Point uses instanceof and ignores color
c.equals(p); // false if ColoredPoint requires instanceof ColoredPoint
             // SYMMETRY BROKEN
```

**Listing 2.** Conceptual: the classic inheritance trap. `getClass()` makes both calls `false` (symmetric, no mixed equality). Making `Point` `final` and using `instanceof` is the other safe pattern. [[How would you explain symmetry requirements for the equals contract in Java]] [[How would you explain pitfalls when implementing equals and hashCode]]

Platform examples:

- `Integer.equals`: true iff the argument is a non-null **`Integer`** with the same `int` — a concrete-type check, not “any `Number`.”
- `List.equals` / `Set.equals`: the other object must be **a list** / **a set**, not the same concrete class — `ArrayList` equals `LinkedList` with the same elements.
- Record `equals`: argument must be an instance of the **same record class**; same components ⇒ same hash.

> [!warning] `getClass()` without a null check
> `if (this.getClass() == that.getClass())` NPEs when `that` is null. `instanceof` already returns false. Do not call `getClass()` on the argument first. And do not mix `instanceof` in the parent with `getClass()` in the child.

> [!tip] Interview answer
> **`instanceof` is “this type or a subtype”; `getClass() ==` is “exactly this class.”** `instanceof` is null-safe. If a subclass adds fields to `equals`, `instanceof` can break symmetry; `getClass()` avoids that by rejecting subclasses. Collections equal across implementations; records require the same record class. There is no single mandated test.
