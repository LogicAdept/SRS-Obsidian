<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/TreeSet #SRS

# What happens when you insert elements into a TreeSet in ascending order?

> [!abstract] Short answer
> **Nothing pathological: the set stays a balanced red-black tree.** `TreeSet` is a `TreeMap`, and `TreeMap` is red-black, so `add` / `contains` / `remove` remain **guaranteed log(n)** even if you insert 1, 2, 3, … in order. Iteration is still sorted by the comparator, not by insertion sequence.

## Sorted inserts are a normal case

A naive binary search tree can become a linked list if keys arrive already sorted. `TreeSet` is not that tree. The class is “based on a `TreeMap`.” `TreeMap` is “a Red-Black tree based `NavigableMap`” (algorithms adapted from Cormen, Leiserson, and Rivest) with **guaranteed log(n)** `put` / `get` / `remove` / `containsKey`. `TreeSet` documents the same bound for `add` / `remove` / `contains` ([[Which tree data structure backs Java TreeSet]]).

Each `add` of a new element still does a logarithmic search plus rebalance (rotations / recoloring), whether keys arrive **ascending, descending, or shuffled**. You do not get amortized O(1) append. You also do not get O(n) `contains`. Height stays Θ(log n).

Stored order is the comparator (or natural order), always **ascending** for `iterator()`. Adding 3 then 1 then 2 yields the same tree shape *family* as adding 1, 2, 3 — red-black, not insertion order. `addFirst` / `addLast` throw `UnsupportedOperationException` ([[When should you choose HashSet LinkedHashSet or TreeSet]]).

```d2
direction: right
ins: "insert 1, 2, 3, …" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
naive: "unbalanced BST\nheight ~ n" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
ts: "TreeSet / TreeMap\nred-black, log(n)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

ins -> naive
ins -> ts
```

**Fig. 1.** Ascending keys are the textbook BST worst case. They are not a `TreeSet` worst case.

```java
NavigableSet<Integer> s = new TreeSet<>();
for (int i = 1; i <= 10_000; i++) {
    s.add(i);
}
s.contains(9_999); // still a tree probe — guaranteed log(n)
s.first();         // 1
s.last();          // 10_000
```

**Listing 1.** Ten thousand ascending inserts. `contains` is not a walk from 1 to 9999. Duplicates still return `false` and do not grow the set.

> [!warning] Do not describe `TreeSet` as “a BST that skews if you insert sorted”
> That is an unbalanced-tree lecture, not `java.util.TreeSet`. After any mix of adds, `iterator()` is comparator order. `LinkedHashSet` is the set that remembers insertion. `TreeSet` compares.

> [!warning] Log(n) is per operation, not “free because it was already sorted”
> Sorted input does not skip rebalancing. If you only need uniqueness and not sorted views, `HashSet` expected-constant `add` is the cheaper structure.

> [!tip] Interview answer
> **Inserting into a `TreeSet` in ascending order does not unbalance it — it is a red-black `TreeMap`, so `add` and `contains` stay log(n).** That is the difference from a lecture BST. Iteration is sorted, not insertion order.
