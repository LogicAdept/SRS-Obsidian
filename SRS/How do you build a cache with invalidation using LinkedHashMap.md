<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Caching #SRS

# How do you build a cache with invalidation using `LinkedHashMap`?

> [!abstract] Short answer
> **Subclass `LinkedHashMap` in access-order, override `removeEldestEntry` so it returns `size() > max` after a new `put`.** Access-order makes eldest = least recently used. Insertion-order plus the same override is FIFO, not LRU. The default `removeEldestEntry` always returns `false`, so a plain `LinkedHashMap` never evicts. The map is still unsynchronized.

## LRU is access-order plus a size cap

The class javadoc calls the `accessOrder` constructor well-suited to LRU caches. `get` / `put` / the other listed access methods move that entry to youngest. Eldest is then the least recently accessed mapping. [[What are LinkedHashMap ordering guarantees]] is that list and which methods count as an access.

`removeEldestEntry` runs from `put` and `putAll` **after a new entry is inserted**. Return `true` and the map removes that eldest. The documented sample keeps a steady 100 entries:

```java
private static final int MAX_ENTRIES = 100;

protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
    return size() > MAX_ENTRIES;
}
```

**Listing 1.** From the `LinkedHashMap.removeEldestEntry` javadoc (Java SE 21). After the 101st **new** key, `size()` is 101, the method returns true, eldest is dropped, size is 100. Use `>` after insert, not `>= MAX` (that would evict on the MAX-th insert).

```d2
direction: down
put: "put of a new key" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ins: "Insert node\n(access-order: tail)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
ask: "removeEldestEntry(head)?" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}
keep: "Keep all entries" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
drop: "Remove eldest\n(LRU / FIFO)" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}

put -> ins -> ask
ask -> keep: false
ask -> drop: true
```

**Fig. 1.** Eviction is hooked to **insert**, not to `get`. A cache hit only relinks the list when `accessOrder` is true.

The method is `protected`, so you subclass (often an anonymous class). Do not mutate the map inside the override and also return `true`: that combination is **unspecified**. If you remove entries yourself, return `false`. The default body returns `false` forever.

Replacing the value of an existing key does not insert a new entry, so it does not consult `removeEldestEntry`. `containsKey` is not an access, so it will not refresh LRU.

## What this cache is not

Insertion-order + `size() > max` evicts the oldest **insert**, even if that key was just read. That is not LRU.

`LinkedHashMap` is not synchronized. A concurrent cache needs an external lock or a concurrent map; this pattern is single-threaded (or externally locked). It has no TTL, no byte-size budget, and no listener beyond what you write in the override.

Java 21 also documents inspecting/removing the current eldest with `firstEntry` / `pollFirstEntry` instead of `removeEldestEntry`. That is another eviction hook, not a different ordering mode.

> [!warning] `new LinkedHashMap<>(16, 0.75f, true)` without the override
> Access-order alone never deletes. You get LRU **iteration**, not a bounded cache. `WeakHashMap` invalidates when the GC clears keys; that is a different policy. [[What is WeakHashMap used for]] is GC-based eviction, not `removeEldestEntry`.

> [!tip] Interview answer
> **For an LRU cache: `new LinkedHashMap<>(cap, 0.75f, true)` and override `removeEldestEntry` to `return size() > max`. Access-order makes eldest the least recently used; the hook runs after each new `put`/`putAll`. Insertion-order gives FIFO. Default `removeEldestEntry` never evicts. Not thread-safe.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как, используя LinkedHashMap, сделать кэш c «invalidation policy»?**

Необходимо использовать _LRU-алгоритм (Least Recently Used algorithm)_ и `LinkedHashMap` с access-order. В этом случае при обращении к элементу он будет перемещаться в конец списка, а наименее используемые элементы будут постепенно группироваться в начале списка. Так же в стандартной реализации `LinkedHashMap` есть метод `removeEldestEntries()`, который возвращает `true`, если текущий объект `LinkedHashMap` должен удалить наименее используемый элемент из коллекции при использовании методов `put()` и `putAll()`.

```java
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private static final int MAX_ENTRIES = 10;

    public LRUCache(int initialCapacity) {
        super(initialCapacity, 0.85f, true);
    }

    @Override
    protected boolean removeEldestEntry(Mindmap.Entry<K, V> eldest) {
        return size() > MAX_ENTRIES;
    }
}
```

Стоит заметить, что `LinkedHashMap` не позволяет полностью реализовать LRU-алгоритм, поскольку при вставке уже имеющегося в коллекции элемента порядок итерации по элементам не меняется.
