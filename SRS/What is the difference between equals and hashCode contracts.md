<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #SRS

# What is the difference between `equals` and `hashCode` contracts?

> [!abstract] Short answer
> `equals` is a **boolean equivalence relation** on object references. `hashCode` is an **`int` that hash tables use to group candidates**. They are coupled one way: equal objects must share a hash; equal hashes do not mean equal objects. `equals` can stand alone as a comparison. `hashCode` is meaningless as a membership test.

## Two different questions

```text
equals(x, y)   →  "same logical value?"     boolean
hashCode(x)    →  "which int bucket hint?"  int
```

**Listing 1.** Roles from the `Object` javadocs. `hashCode` exists for hash tables such as `HashMap`. `equals` defines whether two references count as the same value.

```d2
direction: down
eq: "equals\n5 rules, boolean" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
hc: "hashCode\n3 rules, int" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
link: "equals true  =>  hashes equal\nhashes equal =/=> equals true" {
  width: 340
  height: 90
  style.fill: "#ffe0b2"
}

eq -> link
hc -> link
```

**Fig. 1.** The contracts answer different questions. Only one implication is required.

## What each contract actually lists

`equals` (non-null `x`, `y`, `z`): reflexive, symmetric, transitive, consistent while equality state is unchanged, and `x.equals(null)` is `false`. That is an equivalence relation. [[How would you explain the Object equals method contract]] and [[What properties does an equivalence relation induced by equals have]] unpack those five.

`hashCode`: the same `int` on repeated calls in one run while that `equals` state is unchanged; equal objects produce the same `int`; unequal objects **may** share an `int`. The integer need not be stable across JVM runs. Distinct hashes are recommended for speed, not required. [[How would you explain the hashCode method contract in Java]] is that list.

The `equals` page’s API note is the bridge: if you override `equals`, you generally must override `hashCode` so equal objects keep equal hashes. [[How would you explain the equals and hashCode contract together in Java]] is the pairing; [[Why should equals and hashCode be overridden together]] is why a half-override breaks maps.

## Practical differences

| Concern | `equals` | `hashCode` |
| --- | --- | --- |
| Result | `true` / `false` | any `int` |
| Unique values | partitions objects into classes | 2³² pigeonholes; collisions legal |
| Default `Object` | `x == y` | distinct ints when practical |
| Hash table | decides the mapping | chooses the bin first |

A constant `hashCode` still obeys its contract and wrecks dispersion. A constant `equals` that returns `true` for every pair would break symmetry/transitivity with `null` and with unequal types, and is not a serious implementation. Interview traps: treating a matching hash as equality; requiring unique hashes; claiming `equals` is “for HashMap only” (lists and ordinary `if` use it too).

> [!warning] Do not test equality with `hashCode`
> Matching hashes are **not sufficient** for `equals`. They **are** necessary if `equals` is already true. Do not replace `a.equals(b)` with a hash comparison. Collections still call `equals` after the hash matches. [[What is a hash collision]] is the legal same-hash case.

> [!tip] Interview answer
> **`equals` is the equivalence test (five boolean rules). `hashCode` is a 32-bit hint for hash tables (three integer rules). Equal objects must share a hash; a shared hash does not mean the objects are equal. Override them together when you change value equality; never use `hashCode` as a substitute for `equals`.**
