<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #DSA/Algorithms/Hashing #SRS

# Why is `Point` hashCode `31 * x + y` better than `x + y`?

> [!abstract] Short answer
> **`x + y` does not care which coordinate is which.** If `equals` treats `(1, 2)` and `(2, 1)` as different points, `x + y` still hashes them the same. `31 * x + y` is the two-field form of the platform polynomial (`String`, `List`): order matters, so those two points usually land in different buckets. Distinct hashes for unequal objects are what `Object.hashCode` asks for to keep hash tables fast.

## Addition is commutative; `equals` on a point is not

A typical `Point.equals` is `x == p.x && y == p.y`. Then `(1, 2)` and `(2, 1)` are **unequal**. `1 + 2` and `2 + 1` are **equal**, so every swap is a guaranteed collision. Whole families collide (`(0, 5)`, `(1, 4)`, `(2, 3)`, …). `HashMap` documents that many keys with the same `hashCode()` slow any hash table. [[What happens to HashMap if all keys share the same hashCode]]

`31 * x + y` is `x * 31^1 + y * 31^0` — the `n = 2` case of `String.hashCode`:

```text
String (n chars):  s[0]*31^(n-1) + s[1]*31^(n-2) + … + s[n-1]

Point two ints:    x*31 + y
```

**Listing 1.** Same ordered polynomial. `List.hashCode` is the running form `hash = 31 * hash + field` (seed `1`). `Objects.hash(x, y)` hashes a sequence the same way (via `Arrays.hashCode`). [[How would you explain the hashCode method contract in Java]]

```text
Point(1, 2) vs Point(2, 1)   equals false

x + y                         3 == 3      collision
31 * x + y                    33 != 63    different
```

**Listing 2.** Concrete swap. The multiplier makes the result depend on **which field is in which position**, which is the dump’s “order of processing” idea. [[Why can two unequal objects share the same hashCode value]]

```d2
direction: down
pts: "(1,2) and (2,1)\nequals false" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
sum: "x + y\nsame hash" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
poly: "31*x + y\ndifferent hashes" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

pts -> sum
pts -> poly
```

**Fig. 1.** Unequal points must not be forced into one hash just because addition commutes.

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
        return 31 * x + y;
    }
}
```

**Listing 3.** Conceptual: include the same fields as `equals`, mixed with `31`. `return Objects.hash(x, y);` is the library spelling for several fields. [[What steps must you follow to implement hashCode correctly]] [[Why should equals and hashCode be overridden together]]

> [!warning] `31 * x + y` is not a unique id
> `(0, 31)` and `(1, 0)` both hash to `31`. Collisions remain legal; `equals` still decides. `x ^ y` is commutative too, so it has the same swap bug as `x + y`. Do not invent “31 is magic uniqueness.”

> [!tip] Interview answer
> **Prefer `31 * x + y` because `x + y` collides every swapped point that `equals` treats as different.** That `31` mix is the two-component `String` / `List` hash: field order changes the result. It still collides sometimes; it just does not throw away order.
