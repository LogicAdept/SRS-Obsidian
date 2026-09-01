<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Implementation #SRS

# Can you implement `equals` by comparing only `hashCode` values?

> [!abstract] Short answer
> **No.** Equal hash codes do not imply equal objects. The `hashCode` contract allows collisions among unequal instances, so `return this.hashCode() == that.hashCode()` can return `true` for distinct values and still look “correct” until a collision appears. A compliant `equals` must use identity or field comparison (and return `false` for `null`), then keep `hashCode` compatible with that equality.

## Why hash equality is the wrong test

`hashCode` requires: if `a.equals(b)` is `true`, then the hashes match. The converse is **not** required: unequal objects may share an `int`. That is a legal collision, not a bug. See [[Why can two unequal objects share the same hashCode value]] and [[How would you explain the equals and hashCode contract together in Java]].

```d2
direction: down
sameHash: "a.hashCode() == b.hashCode()" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
mayEq: "May still be a.equals(b) == false" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
eqTrue: "a.equals(b) == true" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
mustHash: "Must have equal hashes" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

eqTrue -> mustHash
sameHash -> mayEq
```

**Fig. 1.** The implication runs only from equality to equal hashes. Hash-only `equals` invents the reverse implication.

```java
public class Main {
    public static void main(String[] args) {
        String a = "Aa";
        String b = "BB";

        System.out.println(a.equals(b));                 // false
        System.out.println(a.hashCode() == b.hashCode()); // true (both 2112)
    }
}
```

**Listing 1.** Java 8+: published `String` collision. A hash-only `equals` would wrongly treat `"Aa"` and `"BB"` as equal.

Any constant `hashCode` is contract-legal and collapses every instance into one hash — hash-only `equals` would then claim every pair is equal.

## Other contract breaks in the naive one-liner

```java
@Override
public boolean equals(Object that) {
    return this.hashCode() == that.hashCode(); // broken
}
```

**Listing 2.** Conceptual anti-pattern. Problems beyond collisions:

* **`null`:** `that.hashCode()` throws `NullPointerException`. The contract requires `x.equals(null)` to be `false`. See [[How would you explain someObj.equals(null)]].
* **Type:** no check that `that` is a compatible type; unrelated classes can share a hash by chance.
* **Symmetry / consistency:** once subclasses override `hashCode` differently, or mutable state changes the hash between calls, results stop matching a stable equivalence relation.

`Object.equals` is identity (`this == obj`), not hash comparison. Default `Object.hashCode` aims for distinct ints **as far as reasonably practical** — not a uniqueness guarantee, and not a specified “memory address” formula. [[How are hashCode and equals implemented in java.lang.Object]] covers that pair.

> [!warning] “It works for plain `Object`” is still wrong
> Even two `new Object()` instances are not promised distinct hashes forever. Identity equality (`==`) is the correct default, not comparing identity hashes. Rare identity-hash collisions would make hash-only `equals` return `true` for unequal references and break reflexivity assumptions of hash tables that already trust `equals`.

## Correct direction

Override `equals` with the fields (or identity) that define sameness; override `hashCode` from a **compatible** set of those fields so equal objects share a hash. Do not derive equality from the hash. [[How do you override equals correctly in Java]] and [[Why should equals and hashCode be overridden together]] are the implementation rules.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof UserId)) return false;
    return value == ((UserId) o).value;
}

@Override
public int hashCode() {
    return Long.hashCode(value);
}
```

**Listing 3.** Conceptual value class: equality from `value`; hash derived from the same field.

> [!tip] Interview answer
> **You must not implement `equals` as “same `hashCode`.”** Collisions are allowed, so equal hashes are only a filter for hash tables, not a proof of equality. Compare identity or the logical fields, return `false` for `null`, and keep `hashCode` consistent with that `equals`.
