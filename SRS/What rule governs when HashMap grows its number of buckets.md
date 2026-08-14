<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# What rule governs when `HashMap` grows its number of buckets?

> [!abstract] Short answer
> **When the number of mappings exceeds `capacity × loadFactor`.** Capacity is bucket count, not `size()`. The table is then rehashed to about twice as many buckets. With the defaults (16 and 0.75) that product is 12, so the first growth is the 13th distinct key. Replacing a value does not grow the table.

## The documented threshold

The `HashMap` javadoc names two parameters: **initial capacity** (buckets at construction, after the table exists) and **load factor** (how full the table may get). Growth is this sentence:

```text
when mappings > loadFactor × current capacity
  → rehash
  → about twice as many buckets
```

**Listing 1.** The public rule (Java SE 21). “Exceeds” is a strict inequality: equality with the product does not yet rehash.

```d2
direction: down
size: "size()\nmappings" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
cmp: "size > capacity × loadFactor ?" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
keep: "Keep this table" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
grow: "Rebuild\n≈ 2 × buckets" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}

size -> cmp
cmp -> keep: no
cmp -> grow: yes
```

**Fig. 1.** Compare mapping count with `capacity × loadFactor`, not with `0.75 × size()`.

OpenJDK keeps that product in `threshold` and, after inserting a **new** key, runs `if (++size > threshold) resize()`. Defaults: capacity 16, load factor 0.75, `threshold` 12. The 12th mapping still fits; the 13th crosses. [[What are the initial capacity and load factor parameters of HashMap]] is how those values are chosen. [[How and when does HashMap resize its buckets]] is allocation, doubling, and the extra Java 8+ path.

If you construct with an initial capacity **greater than** (expected mappings) / loadFactor, the same javadoc says no rehash need ever occur. That is the public way to avoid growth, not a different rule.

## What the rule is not

Capacity is the array length. `size()` is how many keys are stored. Load factor 0.75 does **not** mean “resize at 75% of `size()`” and does not mean every `put`. An overwrite leaves `size` unchanged, so the inequality does not move.

The documented rule is load-factor growth. OpenJDK also calls `resize()` to **create** a still-null table on first `put`, and Java 8+ `treeifyBin` may double a table smaller than 64 buckets instead of converting a crowded list. Those are not the javadoc threshold; they are implementation extra entries into the same method.

> [!warning] “75% full” is a slogan
> For defaults it matches `12 / 16`. Change capacity or load factor and the product changes. The test is still `size > capacity × loadFactor`, integerized as `threshold`.

> [!tip] Interview answer
> **`HashMap` grows when `size` exceeds `capacity × loadFactor`. Capacity is the number of buckets. Defaults 16 and 0.75 give threshold 12, so the 13th new key rehashes to about twice the buckets. Overwrite does not trigger it. That is the public rule; first allocation and Java 8 small-table treeify are separate `resize` calls.**
