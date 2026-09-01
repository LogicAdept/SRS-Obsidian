<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #SRS

# What properties does an equivalence relation induced by `equals` have?

> [!abstract] Short answer
> It is **reflexive, symmetric, and transitive** on non-null references (plus consistency while equality state is unchanged, and `equals(null)` is false). That partitions objects into **equivalence classes**: members of a class are equal to each other and substitutable for the purpose that `equals` encodes. `Object.equals` makes every instance its own class. A value override merges instances into larger classes. `hashCode` must be constant on each class.

## From the five rules to a partition

The `equals` contract requires, for non-null `x`, `y`, `z`:

1. `x.equals(x)`
2. `x.equals(y)` if and only if `y.equals(x)`
3. `x.equals(y)` and `y.equals(z)` imply `x.equals(z)`
4. Repeated calls agree while equality-relevant information is unmodified
5. `x.equals(null)` is `false`

The first three are the mathematical equivalence relation. The specification then says that relation **partitions** the elements into equivalence classes: everyone in a class is equal to everyone else in it, and members are substitutable at least for some purposes. [[How would you explain the Object equals method contract]] is the same list in API order. [[How would you explain symmetry requirements for the equals contract in Java]] is why a one-way `instanceof` check blows the partition. Same-reference `==` cannot be `equals` false if the contract holds; that trap is [[Can different references on object ref0 == ref1 be ref0.equals(ref1 == false]]. Value equality is [[How do you override equals correctly in Java]].

```d2
direction: down
objs: "Non-null instances" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
p: "equals partitions" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
c1: "Class {a}" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
c2: "Class {b, b2}" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
c3: "Class {c}" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}

objs -> p
p -> c1
p -> c2
p -> c3
```

**Fig. 1.** Identity `equals` yields singleton classes. Value `equals` may put `b` and `b2` in one class; then they must share `hashCode`.

Under `Object.equals`, each class has a **single** element (`x == y`). That is the most discriminating relation. Your override may only **merge** classes, never split the same instance into two (reflexivity) or put `a` with `b` but not `b` with `a` (symmetry).

## What the partition buys collections

A `HashSet` keeps at most one representative per class: `add` of an equal key does not grow `size`. `HashMap` replaces the value for that class. Both require `hashCode` identical throughout a class; otherwise an equal object hashes to another bin and the partition is not visible to the table. [[Why should equals and hashCode be overridden together]] is that break. [[How would you explain HashSet, hashCode]] is membership under that pair.

Consistency is not “immutable forever.” The class may change when you mutate equality state — the partition is then a different relation. Hash tables do not re-place the object. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is that mismatch.

A `Comparator`’s `compare == 0` is another equivalence (the quotient of the order). It coincides with `equals`’s partition only when the comparator is consistent with equals. [[How does Java decide whether two objects are equivalent]] distinguishes those relations.

> [!warning] Breaking one axiom wrecks the partition
> Fail symmetry and “are these the same class?” depends on which object you ask. Fail transitivity and `Set` can contain `a` and `c` that should have been one element via `b`. `float` primitive `==` is not an equivalence (`NaN`); that is why field comparison uses representation equivalence.

> [!warning] `equals(null)` vs calling equals **on** null
> `x.equals(null)` must return **`false`**, not throw. `null.equals(x)` is a `NullPointerException` — there is no receiver. A type test via `instanceof` is already false for `null`. [[How would you explain someObj.equals(null)]]

> [!tip] Interview answer
> **`equals` must be an equivalence relation: reflexive, symmetric, transitive. It cuts the heap into classes of interchangeable values. `Object` uses singleton classes (identity). A value override merges instances and then every member of a class must share one `hashCode`. Consistency holds only while equality state is unchanged.**
