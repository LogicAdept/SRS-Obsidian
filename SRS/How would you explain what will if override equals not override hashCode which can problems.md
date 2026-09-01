<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Collections/Map/HashMap #Java/Collections/Set/HashSet #SRS

# What goes wrong if you override `equals` but not `hashCode`?

> [!abstract] Short answer
> **Equal copies get different hashes, so hash tables miss them.** `Object.equals` says you generally must override `hashCode` with `equals`. Leave the identity `hashCode`, and `a.equals(b)` can be true while `a.hashCode() != b.hashCode()`. `HashMap.get` / `HashSet.contains` hash first and never look in the bucket that holds the original.

## The contract you just broke

`Object.hashCode`: if `a.equals(b)`, then `a.hashCode() == b.hashCode()`. Default `hashCode` is a native identity int (`System.identityHashCode`). A value `equals` on fields does **not** change that number. Two `new Point(1, 2)` are equal by your method and unequal by hash. [[Why should equals and hashCode be overridden together]] [[How would you explain if equals override are there which methods should you override]] [[How are hashCode and equals implemented in java.lang.Object]]

`Map` implementations may skip `equals` when hashes already differ — that is legal **because** the spec says unequal hashes ⇒ not `equals`. After you violate the pair, that optimization is wrong: the equal key is sitting in another bin. [[How would you explain the hashCode method contract in Java]]

```text
put(new Point(1,2), "v")     bucket ← identity hash of instance A
get(new Point(1,2))          bucket ← identity hash of instance B
                             A.equals(B) == true
                             hashes differ  →  miss

HashSet.add(A); contains(B)  same miss
A.equals(B)                  still true in a unit test
```

**Listing 1.** Direct `equals` passes; hashed lookup fails. [[How would you explain HashSet, hashCode]]

A `Collection.contains` specified only as `Objects.equals` (array list scan) can still find `B`. The bug is **hash-based** structure, not every collection. `HashMap` and `HashSet` are the interview examples.

```d2
direction: down
eq: "value equals true\nidentity hashes differ" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
hm: "HashMap / HashSet\nwrong bucket → miss" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
list: "equals-only scan\nstill finds" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

eq -> hm
eq -> list
```

**Fig. 1.** Same objects, two lookup styles. Only hashing assumed the contract.

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
    // hashCode inherited — identity
}

Point a = new Point(1, 2);
Point b = new Point(1, 2);
a.equals(b); // true
Map<Point, String> m = new HashMap<>();
m.put(a, "v");
m.get(b);    // typically null
```

**Listing 2.** Conceptual: the textbook `HashMap` miss. Add `hashCode` on `x` and `y` (`31 * x + y` / `Objects.hash`) and `get(b)` hits. [[How do you override equals correctly in Java]]

> [!warning] Green tests, broken cache
> Tests that only call `equals` never see this. A cache, intern table, or `HashSet` of “already seen” value objects silently grows duplicates and cannot `get` what you `put`. `@Override` on `hashCode` is the cheap catch. Records already generate **both**.

> [!tip] Interview answer
> **You break “equal objects, equal hashes.”** `HashMap`/`HashSet` locate by `hashCode` then `equals`, so a second equal instance hashes somewhere else and is not found. `equals` itself still looks fine. Always override `hashCode` with `equals`.
