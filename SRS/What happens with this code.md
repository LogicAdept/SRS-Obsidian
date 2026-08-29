<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Career/Interview/Exercises #SRS

# What happens with this code?

> [!abstract] Short answer
> The snippet is an **`ArrayList`**: enhanced-`for` **`add(0, …)`**, then an **index** loop that **`add`s while `i < size()`**. The **first** loop uses a **fail-fast iterator**. `add` is a **structural modification**, so the iterator throws **`ConcurrentModificationException`** (typically on the **next** `next()`, still in that loop). **`list.get(1)` never runs.** The **second** loop is **not** reached. If you ran **only** the index loop, `size()` **grows by 1** each time `i` does, so the condition **never fails** until the list **cannot grow** → **`OutOfMemoryError`**, not CME. CME: [[What is ConcurrentModificationException]]. Single-thread CME: [[How can a single-threaded program get ConcurrentModificationException]]. Fail-fast: [[What is fail-fast iterator behavior in Java collections]]. Structural mod: [[What counts as a structural modification for fail-fast iterators]]. Avoid: [[How do you avoid ConcurrentModificationException while iterating a collection]].

## Iterator vs `size()` in the condition

Enhanced-`for` on `ArrayList` is `iterator()`. After `list.add(0)`, **`modCount`** changes. The iterator then fails **best-effort**; do **not** write logic that **depends** on CME. Fail-fast vs fail-safe: [[What is the difference between fail-fast and fail-safe iterators]].

An **index** loop is **not** an iterator. `add(0, 2)` is **O(n)** per call and **unbounded** growth. The ceiling is **heap / max array length**, not “until `Integer.MAX_VALUE` iterations of `i` stay safe.”

```java
List<Integer> list = new ArrayList<>();
list.add(0);
for (Integer integer : list) {   // iterator
    list.add(0, 1);              // CME (best-effort)
}
for (int i = 0; i < list.size(); i++) {
    list.add(0, 2);              // if reached: grows forever → OOME
}
System.out.println(list.get(1)); // not reached
```

**Listing 1.** First loop aborts the method. Comment it out to see the second loop exhaust memory.

```d2
direction: down
fe: "enhanced-for + add" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
cme: "ConcurrentModificationException" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
ix: "i < size(); add" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
oom: "OutOfMemoryError" {
  width: 180
  height: 36
  style.fill: "#f3e5f5"
}
fe -> cme
ix -> oom: "if that loop runs"
```

**Fig. 1.** CME is the iterator. The index loop’s “infinity” is **memory**.

> [!warning] CME does not mean another thread
> One thread that **mutates** a list while using its **fail-fast iterator** is enough.

> [!warning] Do not treat CME as a control-flow API
> Fail-fast is **best-effort**. The quiz answer is still “first loop throws”; production code should not **require** that throw.

> [!tip] Interview answer
> The for-each add hits ConcurrentModificationException because ArrayList iterators are fail-fast. The indexed loop would never finish because size grows with i, and it would die with OutOfMemoryError. println never runs.
