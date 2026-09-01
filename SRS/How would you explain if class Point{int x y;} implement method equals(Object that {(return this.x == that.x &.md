<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Map/HashMap #Java/HashCodeEquals/Implementation #SRS

# Can a `Point` with `equals` on `x,y` and `hashCode` of only `x` work in a `HashSet`?

> [!abstract] Short answer
> **Yes for correctness, no for speed — if `equals` actually compiles.** `hashCode` may use a **subset** of the `equals` fields. Equal points (same `x` and `y`) still share a hash. Unequal points with the same `x` **collide**, so `HashSet` (a `HashMap`) still separates them with `equals`, but that bucket gets slow. `return x` is legal; `31 * x + y` is what you want.

## Contract versus the dump snippet

`equals(Object that) { return this.x == that.x && this.y == that.y; }` **does not compile**: `Object` has no `x` / `y`. You need `instanceof` (or `getClass`) and a cast. Assume a real `equals` on both coordinates. [[How do you override equals correctly in Java]]

`hashCode` returning only `x` obeys `Object.hashCode`: if `a.equals(b)` then both have the same `x`, so the same hash. It is the **subset** case: legal, more collisions. Using a field `equals` ignores would be the break. [[How would you explain which fields should be included when implementing hashCode in Java]] [[Why should equals and hashCode be overridden together]]

```text
Point(1, 2) and Point(1, 3)
  equals          false
  hashCode        both 1     → same bucket
  HashSet.add     both stay  → two elements
  contains each   true       → equals tells them apart

Point(1, 2) and Point(1, 2)
  equals          true
  hashCode        both 1
  HashSet.add     one element
```

**Listing 1.** Correctness is `equals` after the hash. Same `x` is a collision, not a duplicate. [[How would you explain HashSet, hashCode]] [[Why can two unequal objects share the same hashCode value]]

`HashSet` is backed by `HashMap`. `add` / `contains` / `remove` use `Objects.equals` once hashing has picked a bin. Many keys with the same `hashCode()` slow any hash table. `Point` is not `Comparable`, so the “comparison order to break ties” mitigation does not apply. [[What happens to HashMap if all keys share the same hashCode]] [[How is HashSet implemented in terms of HashMap]]

```d2
direction: down
p: "Points with same x\ndifferent y" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
ok: "equals false\nboth in the HashSet" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
slow: "one bucket does all\nthe equals work" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

p -> ok
p -> slow
```

**Fig. 1.** Subset `hashCode` keeps the set right and throws away dispersion.

```java
final class Point {
    final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Point)) {
            return false;
        }
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return x; // legal subset — prefer 31 * x + y
    }
}

Set<Point> set = new HashSet<>();
set.add(new Point(1, 2));
set.add(new Point(1, 3)); // true — not equals, same hash
set.contains(new Point(1, 2)); // true
set.size(); // 2
```

**Listing 2.** Conceptual: put and get work; every `Point` with `x == 1` shares a bin. [[What steps must you follow to implement hashCode correctly]]

> [!warning] “Degenerates to a linked list”
> Interview shorthand for “all the same hash.” The spec says **slow**, not a particular chain shape. Do not paste internal `e.hash == hash && key.equals(k)` as if it were the `HashSet` contract — `contains` is `Objects.equals` after hashing. And do not ship `that.x` on an `Object` parameter.

> [!tip] Interview answer
> **They still go in and come out of a `HashSet` if `equals` compares `x` and `y` correctly.** Hashing only `x` is a legal subset: equal points match, unequal points with the same `x` collide and `equals` separates them. You pay in speed. Mix **both** fields (`31 * x + y`). The snippet as written does not compile.
