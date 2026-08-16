<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# What are the initial capacity and load factor parameters of `HashMap`?

> [!abstract] Short answer
> **The two performance knobs on a `HashMap`.** Capacity is the **number of buckets**, not `size()`. Initial capacity is that count when the table is created. Load factor is how full the table may get before it is rebuilt with about twice as many buckets. Defaults: **16** and **0.75**. Size the initial capacity from expected mappings so you avoid rehash; do not make it huge if you iterate. Growth rule: [[What rule governs when HashMap grows its number of buckets]].

## What each number is

The class javadoc: an instance has **initial capacity** and **load factor**. Capacity = buckets. Load factor = how full before capacity increases automatically. When mappings **exceed** `loadFactor × current capacity`, the table is rehashed to about twice the buckets.

```text
HashMap()                         capacity 16,  load 0.75
HashMap(n)                        capacity n,   load 0.75
HashMap(n, f)                     capacity n,   load f
HashMap(m)                        load 0.75, capacity enough for m
HashMap.newHashMap(numMappings)   load 0.75, capacity for that many (since 19)
```

**Listing 1.** Constructors (Java SE 21). `HashMap(n, f)` throws `IllegalArgumentException` if `n < 0` or `f` is nonpositive. `HashMap(n)` throws if `n` is negative.

```d2
direction: down
cap: "capacity\n= bucket count" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
lf: "load factor\nhow full before grow" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
thr: "threshold ≈ capacity × loadFactor\nresize when size exceeds it" {
  width: 320
  height: 80
  style.fill: "#ffe0b2"
}
cap -> thr
lf -> thr
```

**Fig. 1.** The knobs set the threshold. They are not `size()`. [[How and when does HashMap resize its buckets]]

Default 0.75 is the documented time/space tradeoff. **Higher** load factor: less space, more collisions, slower `get`/`put`. **Lower**: more empty buckets, faster lookups, slower iteration (iteration is **capacity plus size**). Do not set initial capacity too high or load factor too low if you walk `keySet` / `values` / `entrySet`.

## How to choose them

Take the expected number of mappings and the load factor into account so rehashes stay rare. If initial capacity is **greater than** (maximum entries) / load factor, the javadoc says **no rehash need ever occur**. Pre-sizing many mappings is cheaper than growing as you `put`. `newHashMap(numMappings)` exists so you do not compute that capacity by hand.

OpenJDK rounds the requested capacity up to a power of two when the table is allocated. The public API still talks in “number of buckets,” not in that rounding.

Identical `hashCode()` values still slow the table no matter how large you set capacity. These two parameters do not fix a bad hash. [[What happens to HashMap if all keys share the same hashCode]]

> [!warning] `new HashMap<>(expectedSize)`
> That argument is **buckets**, not “I will insert this many keys.” For load 0.75 you need buckets **> expectedSize / 0.75**, or use `newHashMap`. Passing `100` for 100 keys still rehashes.

> [!tip] Interview answer
> **Initial capacity is starting bucket count (default 16). Load factor is how full before doubling (default 0.75). Size capacity from expected entries / load factor to skip rehash. Oversized capacity hurts iteration. Negative capacity or nonpositive load factor is `IllegalArgumentException`.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**load factor и resize.**

Порог 0.75 по умолчанию. При size >= capacity * loadFactor — resize: массив вдвое + перехеширование ВСЕХ элементов (дорого!). Совет: если знаешь количество элементов — задай initialCapacity = expectedSize / 0.75 + 1.

**Что такое load factor?**

Порог заполнения, по умолчанию 0.75. При size >= capacity * loadFactor происходит resize: новый массив вдвое больше + перехеширование всех элементов.

**Что такое load factor?**

Порог заполнения, по умолчанию 0.75. При size >= capacity * loadFactor — resize: новый массив вдвое больше + перехеширование всех элементов.

**Что такое load factor?**

Соотношение size / capacity, при котором происходит расширение таблицы. По умолчанию 0.75. То есть когда size превышает 75% от capacity, таблица расширяется в 2 раза и все элементы перехэшируются. Уменьшение load factor — меньше коллизий, больше памяти. Увеличение — наоборот.

**Что такое load factor?**

Порог заполнения (по умолчанию 0.75), при котором происходит resize — удвоение массива и rehashing всех элементов.

**load factor и resize.**

0.75 по умолчанию. size >= capacity * loadFactor → resize (вдвое + перехеширование всех). Совет: initialCapacity = expectedSize / 0.75 + 1.

**load factor и resize.**

Порог 0.75. При size >= capacity * loadFactor — resize: массив вдвое + перехеширование ВСЕХ элементов. Совет: initialCapacity = expectedSize / 0.75 + 1.
