<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language/Records #SRS

# How would you explain which fields should be included when implementing `hashCode` in Java?

> [!abstract] Short answer
> Include the fields that **`equals` uses to decide logical identity** — typically exactly those fields. A subset still keeps “equal objects, equal hashes,” but collides more. A field that `equals` **ignores** must not affect `hashCode` if two equal instances can disagree on it. Derived values that are functions of already-included fields add no new contract strength.

## The contract picks the fields

If `a.equals(b)` is true, `a.hashCode()` and `b.hashCode()` must be the same integer. Therefore every piece of state that can make `equals` return `false` is a candidate for the mix, and every piece that `equals` does not consult is a hazard if it can differ. [[How would you explain the hashCode method contract in Java]] is that implication. [[How do you override equals correctly in Java]] is how those fields were chosen.

```d2
direction: down
eq: "Fields used by equals" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
same: "Use the same set\n(usual choice)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
sub: "Subset\nlegal, more collisions" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
extra: "Field equals ignores\nillegal if it can differ" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

eq -> same
eq -> sub
eq -> extra
```

**Fig. 1.** `hashCode` may be weaker than `equals`. It must not be sensitive to state `equals` does not care about.

```text
equals uses {id, name}     → hashCode should mix id and name
equals uses {id} only      → do not mix name (equal ids could disagree)
equals uses {id, name}     → hashing only id is legal, just clumpier
```

**Listing 1.** Same set, subset, forbidden extra field.

`Objects.hash` / `Arrays.hashCode` only help **combine** the fields you already selected. They do not decide which fields belong. [[What steps must you follow to implement hashCode correctly]] is the mechanical mix.

## What to leave out

Skip fields that are not part of value identity: caches, logging counters, “last access” timestamps, monitor state, or `System.identityHashCode` when `equals` is value-based. Skip a derived field that is a pure function of fields you already mix (`fullName` built from `first` and `last`) unless you dropped the originals; hashing both is redundant, not a second contract.

If `equals` compares array **contents**, hash the contents (`Arrays.hashCode` / `deepHashCode`), not the array reference. If `equals` uses representation-equivalent `float`/`double`, use `Float.hashCode` / `Double.hashCode`, not a truncated `(int) x`.

Mutable fields that participate in `equals` **must** participate in `hashCode` (otherwise equal instances can disagree after a mutation of the omitted field). The practical rule is: do not then use that object as a `HashMap` / `HashSet` key. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is the lost-entry failure.

A `record` hashes its components, which are also what its `equals` compares. Business entities that equal by database id only should hash that id, not every column. [[In a business context must equals consider all entity fields]] is that policy.

> [!warning] Extra field is the silent contract break
> Two `Point`s equal on `(x, y)` but `hashCode` mixing a `color` that `equals` ignores will disagree whenever colors differ. Hash tables then fail to find the equal key. The opposite mistake — hashing only `x` when `equals` uses `x` and `y` — is legal, just a [[What is a hash collision]] factory.

> [!tip] Interview answer
> **Hash the same state `equals` uses. A subset is allowed and only costs collisions. A field `equals` ignores is not allowed if equal objects can differ on it. Do not hash identity, caches, or array references when equality is by value. Mutable equals-fields belong in `hashCode`, but then the object is a poor map key.**
