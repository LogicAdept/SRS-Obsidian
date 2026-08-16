<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Versions/8 #SRS

# How many new objects may be allocated when inserting a new entry into `HashMap`?

> [!abstract] Short answer
> **Usually one: a `Node`.** Overwrite allocates nothing. The first `put` also allocates the `Node[]` table. A load-factor (or small-table treeify) resize allocates **one new array** and **reuses** existing nodes. Java 8+ treeification allocates a `TreeNode` per entry in that bin, so one insert can create many objects. The key and value are stored by reference; `HashMap` does not copy them.

## The common path is one `Node`

`put` of a **new** key ends in `newNode` → `new Node<>(hash, key, value, next)`. That is one object. An empty bucket and a list collision both take this factory. A `put` that only replaces the value writes `e.value` and returns — **zero** map-owned objects.

```java
if ((p = tab[i = (n - 1) & hash]) == null)
    tab[i] = newNode(hash, key, value, null);
else if (/* not the same key */)
    p.next = newNode(hash, key, value, null);
```

**Listing 1.** Conceptual OpenJDK `putVal` (Java 21). `newNode` is `new Node<>(…)`. `LinkedHashMap` overrides it to an `Entry`, still one object.

```d2
direction: down
put: "put of a new key" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
node: "1 × Node (or TreeNode)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
table: "maybe 1 × Node[]\nfirst alloc or resize" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
tree: "maybe N × TreeNode\nreplace the whole bin" {
  width: 280
  height: 80
  style.fill: "#ffe0b2"
}
none: "overwrite\n0 objects" {
  width: 220
  height: 70
  style.fill: "#eeeeee"
}

put -> node
put -> table
put -> tree
put -> none
```

**Fig. 1.** Count map-owned objects, not the key/value you already built. [[What is the internal structure of HashMap]]

The public `put` javadoc does not mention allocation. It only says a new mapping is associated, or an old value is replaced.

## When the count is not one

**First insert.** The no-arg constructor leaves `table` null. `putVal` calls `resize()` before `newNode`. Default: one `Node[16]` **plus** one `Node`.

**Resize.** After `++size > threshold`, `resize` does `new Node[newCap]` and **moves** existing `Node`s. It does not clone them. Cost of that `put`: the new entry’s `Node` plus **one array object** (the old array becomes garbage). Same extra array if Java 8+ `treeifyBin` resizes a table smaller than 64 instead of converting. [[How and when does HashMap resize its buckets]]

**Treeify (Java 8+, table already ≥ 64).** `putVal` still allocates the new `Node`, then `treeifyBin` walks the bin and `replacementTreeNode`s every entry — a **new `TreeNode` per node in that bin** (9 when the 9th is added). The plain `Node`s, including the one just created, become unreachable. Insert into an **already** tree-shaped bin uses `newTreeNode` once (`putTreeVal`), not a full rewrite. [[How does HashMap handle collisions]]

```text
overwrite existing key          0
new key, table already there    1 Node
first put (defaults)            1 Node[] + 1 Node
new key + doubling resize       1 Node + 1 Node[]
9th in a list, cap ≥ 64         1 Node + 9 TreeNode  (old Nodes discarded)
new key in a tree bin           1 TreeNode
```

**Listing 2.** OpenJDK `HashMap` object counts for one `put`. Array length is not “16 objects”; a `Node[]` is one object.

> [!warning] Not “one object per bucket” and not the key
> Interview answers that say “always 1” skip first allocation, resize, and treeify. Answers that count the key, the value, or autoboxed `Integer`s are counting the caller’s objects. `HashMap` holds references. `size()` is mappings, not JVM objects.

> [!tip] Interview answer
> **A new mapping is normally one `Node`. Overwrite is zero. The first `put` also allocates the table array; a resize allocates a larger array and reuses nodes. Treeifying a bin allocates a `TreeNode` for every entry in that bucket. Keys and values are not copied.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Сколько создается новых объектов, когда вы добавляете новый элемент в `HashMap`?**

__Один__ новый объект статического вложенного класса `Entry<K,V>`.
