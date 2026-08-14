<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language/Records #Java/Versions/16 #SRS

# Why should `equals` and `hashCode` be overridden together?

> [!abstract] Short answer
> Because hash tables assume **equal objects have equal hashes**. The `equals` API says that if you override `equals`, you generally must override `hashCode` too. Overriding only `equals` leaves the identity-based `Object.hashCode`, so two value-equal instances usually land in **different** buckets and `HashMap`/`HashSet` cannot find the other. Overriding only `hashCode` while keeping identity `equals` does not create value equality and still surprises if the new hash is unstable.

## The one-way rule hash tables rely on

`hashCode` requires: if `a.equals(b)` is true, both hashes are the same `int`. [[How would you explain the equals and hashCode contract together in Java]] is the full pairing. Inherited `Object` satisfies it: `equals` is `==`, and `hashCode` is (as far as practical) distinct per object. You may keep both defaults. You may not change one side of that pair and leave the other on identity.

```d2
direction: down
eq: "Override equals\n(value equality)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
hc: "Must override hashCode\nfrom the same fields" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
skip: "Keep Object.hashCode" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
lost: "Equal keys, different buckets\nget/contains miss" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

eq -> hc
eq -> skip -> lost
```

**Fig. 1.** Value `equals` without a matching `hashCode` is the classic lost-key bug.

`HashMap.get` indexes by mixed `hashCode`, then confirms with identity or `equals`. If two equal keys have different hashes, the search never looks in the bucket where the first key was stored. [[Is equals invoked when a HashMap bucket contains a single element]] still runs `equals` only **after** the stored hashes match.

## What each half-override does

**`equals` only.** Two `Name("Ada")` instances compare equal, but each typically has a different identity hash. `set.add(a)` then `set.contains(b)` can be false even though `a.equals(b)` is true. `HashSet` is a `HashMap` underneath, so the same miss happens for map keys.

**`hashCode` only.** `equals` remains identity. Hash tables still treat `a` and `b` as different keys unless they are the same reference. You paid for a custom mix that `equals` will never treat as the same object. If that mix uses mutable state, you can also lose the original reference after mutation. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is that second failure.

```java
@Override
public boolean equals(Object o) { /* value fields */ }

@Override
public int hashCode() { /* the same fields */ }
```

**Listing 1.** The required pair. [[What steps must you follow to implement hashCode correctly]] and [[How do you override equals correctly in Java]] are the two implementations.

A `record` already overrides both from its components. Do not override one component-based method and leave the other.

> [!warning] “They equal in my test, so the set contains them”
> Direct `a.equals(b)` does not exercise the hash table. Always check `HashSet.contains` / `HashMap.get` with a **second** instance. Interview answers that say “override `equals` for HashMap” and stop are incomplete.

> [!tip] Interview answer
> **Override them together, or override neither.** Hash-based collections find a candidate bucket from `hashCode` and only then call `equals`. Value equality with the default identity hash puts equal objects in different buckets, so lookup misses. The `equals` javadoc already tells you to keep `hashCode` in contract.
