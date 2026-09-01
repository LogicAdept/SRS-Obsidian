<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Contract #SRS

# If you override `equals`, which other methods must you override?

> [!abstract] Short answer
> **`hashCode`.** Equal objects must produce equal hashes. `Object.equals` says it is generally necessary to override `hashCode` whenever you override `equals`. `toString` is optional. `compareTo` is only in play if the class is `Comparable` — then keep it **consistent with `equals`**, but that is not a second mandatory override for every value type.

## The required pair

`Object.hashCode`: if `a.equals(b)`, then `a.hashCode() == b.hashCode()`. Leave the identity `hashCode` while you write a value `equals`, and two equal instances get **different** hashes. `HashSet` / `HashMap` then look in the wrong bucket and `contains` misses. [[Why should equals and hashCode be overridden together]] [[How would you explain the hashCode method contract in Java]] [[How would you explain HashSet, hashCode]]

```text
override equals(Object)     →  also override hashCode()
                               use the same fields (or a subset)

do not have to override     →  toString, clone, compareTo
compareTo                   →  only if you implement Comparable;
                               then strongly recommended:
                               compareTo == 0  ⇔  equals
```

**Listing 1.** One required partner; one conditional consistency rule. [[How would you explain which fields should be included when implementing hashCode in Java]] [[How do you override equals correctly in Java]]

```java
final class Point {
    final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Point p)) {
            return false;
        }
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return 31 * x + y;
    }
}
```

**Listing 2.** Conceptual: the pair. Drop `hashCode` and `new HashSet<Point>()` will not treat two `Point(1, 2)` as the same element. `Objects.hash(x, y)` is the multi-field helper. Records already synthesize **both** from every component. [[Why are Java records good HashMap keys]]

```d2
direction: down
eq: "override equals" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
hc: "must override hashCode" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
cmp: "if Comparable:\nalign compareTo" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

eq -> hc
eq -> cmp
```

**Fig. 1.** `hashCode` is the contract partner. `compareTo` is only for types that define an order.

`Comparable`: natural order is consistent with `equals` iff `e1.compareTo(e2) == 0` has the same boolean value as `e1.equals(e2)`. Strongly recommended, not required — sorted sets/maps without a comparator **violate the `Set`/`Map` contract** when it is inconsistent (second `add` ignored). [[Why must TreeMap ordering be consistent with equals]] `BigDecimal` is the documented core exception (numeric vs representation equality).

> [!warning] `equals` alone is the `HashSet` bug
> Overriding only `equals` looks fine in unit tests that call `a.equals(b)` and then fails in a hash table. `@Override` on `hashCode` is the cheap reminder. Do not “also override `compareTo`” on a class that is not ordered — that is a different interface.

> [!tip] Interview answer
> **Always override `hashCode` with `equals` — equal objects must hash equal, or `HashMap`/`HashSet` break.** `toString` is courtesy, not the contract. If the class is `Comparable`, keep `compareTo` consistent with `equals` for `TreeSet`/`TreeMap`; that is strongly recommended, not a third method every `equals` must grow.
