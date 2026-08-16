<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/LinkedHashMap #Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS

# How do `HashMap`, `TreeMap`, and `LinkedHashMap` differ at a high level?

> [!abstract] Short answer
> **`HashMap` hashes, order unspecified. `LinkedHashMap` is a `HashMap` plus a doubly-linked list that defines encounter order (insertion-order by default, or access-order). `TreeMap` is a red-black tree, sorted by key, guaranteed log(n).** All three are unsynchronized `Map`s. `LinkedHashMap` keeps `HashMap`-like expected constant-time lookup without `TreeMap`’s sort cost. Iteration of `LinkedHashMap` is proportional to **size**, not capacity.

## Three answers to “in what order?”

```text
HashMap         no order (may change over time)
LinkedHashMap   encounter order: insertion, or last access
TreeMap         sorted by Comparable / Comparator
```

**Listing 1.** The usual interview split, from the three class javadocs (Java SE 21). `LinkedHashMap` says it spares you `HashMap`’s chaotic order without `TreeMap`’s extra cost.

```d2
direction: down
q: "Which Map?" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
sort: "Need keys sorted\nor ranges?" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
enc: "Need a defined\niteration order?" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
tm: "TreeMap" {
  width: 180
  height: 60
  style.fill: "#ffe0b2"
}
lhm: "LinkedHashMap" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
hm: "HashMap" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}

q -> sort
sort -> tm: yes
sort -> enc: no
enc -> lhm: yes
enc -> hm: no
```

**Fig. 1.** Sort vs encounter order vs “I do not care.” Do not use `TreeMap` to “keep insertion order.”

`LinkedHashMap` **extends** `HashMap`. Re-`put` of an existing key does **not** move it in insertion-order. A special constructor switches the list to access-order (LRU-style). [[What are LinkedHashMap ordering guarantees]] and [[How do you build a cache with invalidation using LinkedHashMap]] are those modes. Copying `new LinkedHashMap<>(m)` is the documented way to snapshot another map’s iteration order.

## Lookup, keys, nulls

`HashMap` and `LinkedHashMap` both document constant-time basic operations **assuming** hashes disperse. `LinkedHashMap` is slightly slower because of the list, except iteration: it walks the list (time ~ size), while `HashMap` walks the table (capacity + size). [[What is the internal structure of HashMap]] is the shared bin array. [[How do HashMap, TreeMap, and LinkedHashMap work at a high level]] is the three internals in one place.

`TreeMap` does not hash. It guarantees log(n) `get`/`put`/`remove` on a red-black tree. Keys must be comparable; ordering should be consistent with `equals`. [[Compare HashMap and TreeMap tradeoffs]] is that pair. [[What data structure backs TreeMap in Java]] is the tree.

`HashMap` and `LinkedHashMap` permit a `null` key and `null` values. `TreeMap` rejects a `null` key under natural ordering.

> [!warning] Three maps, three orders
> “Ordered `HashMap`” is not `TreeMap`. Sorted order is by key comparison. Encounter order is the linked list. Unspecified order is plain `HashMap`. Access-order `get` is a structural modification on `LinkedHashMap`; insertion-order `get` is not.

> [!tip] Interview answer
> **`HashMap`: hash table, unspecified order, expected O(1) if hashes spread. `LinkedHashMap`: same table plus a doubly-linked list for insertion-order (or access-order) iteration in O(size). `TreeMap`: red-black `NavigableMap`, sorted keys, guaranteed log(n). Choose by whether you need no order, encounter order, or sort order.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**HashMap vs TreeMap vs LinkedHashMap.**

HashMap — быстрый, без порядка. TreeMap — отсортирован по ключам, O(log n). LinkedHashMap — сохраняет порядок вставки или access order.

**HashMap vs TreeMap vs LinkedHashMap.**

HashMap — хэш, без порядка, O(1). TreeMap — красно-чёрное дерево, отсортирован по ключам, O(log n). LinkedHashMap — сохраняет порядок вставки или access order.

**HashMap vs TreeMap vs LinkedHashMap — когда что?**

HashMap — быстрый доступ без порядка. TreeMap — сортировка ключей, O(log n). LinkedHashMap — сохраняет порядок вставки или access order.

**HashMap vs Hashtable vs LinkedHashMap vs WeakHashMap.**

HashMap: не потокобезопасен, null-ключ. Hashtable: потокобезопасен (synchronized на всё), устаревший, нет null. LinkedHashMap: порядок вставки (или access order для LRU). WeakHashMap: ключи через WeakReference — GC собирает неиспользуемые записи (для кэшей). ConcurrentHashMap — замена Hashtable.
