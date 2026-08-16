<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/Collections/Concurrency #Java/Concurrency #SRS

# Is `java.util.HashMap` thread safe?

> [!abstract] Short answer
> **No.** The class javadoc states the implementation is **not synchronized**. If several threads use the same map and at least one of them modifies it structurally (add or delete a mapping), you must synchronize externally. Replacing the value of a key that is already present is not a structural modification in that sentence. Concurrent unsynchronized use is not a supported mode; iterators are fail-fast only on a best-effort basis.

## What the spec requires

```text
HashMap
  not synchronized
  concurrent access + structural modify
    → synchronize on an encapsulating lock
    → or Collections.synchronizedMap(new HashMap<>(...))
      (wrap at creation)
```

**Listing 1.** The `HashMap` class javadoc (Java SE 21). Structural modification = add or delete mappings, including rehash.

```d2
direction: down
q: "Shared hash map?" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
one: "One thread\nor immutable after publish" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
wrap: "Collections.synchronizedMap" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
chm: "ConcurrentHashMap" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}

q -> one: no concurrent writers
q -> wrap: coarse lock on HashMap
q -> chm: concurrent updates
```

**Fig. 1.** `HashMap` is the single-threaded (or externally locked) table. A concurrent map is a different class.

Fail-fast iterators throw `ConcurrentModificationException` if the map is structurally modified after the iterator is created, except via that iterator’s `remove`. The javadoc warns that this **cannot be guaranteed** under unsynchronized concurrent mutation and must not be used as a lock. [[How can misuse of HashMap lead to an infinite loop]] is what can happen when two threads resize without a lock — that is not a specified API, just why “undefined” is not theoretical.

## What to use instead

`Collections.synchronizedMap` locks every method on one mutex. Compound actions (`containsKey` then `put`) still need the same lock around the whole sequence.

`Hashtable` is synchronized and forbids nulls. Its own javadoc tells you to use `HashMap` when you do not need thread safety, and `ConcurrentHashMap` when you do. [[What is the difference between HashMap and Hashtable]] is that pair. [[How does Hashtable differ from ConcurrentHashMap]] is the concurrent replacement.

`ConcurrentHashMap` supports concurrent retrievals (typically without locking the whole table) and high expected concurrency for updates. It matches `Hashtable`’s functional spec in that sense, **does not allow null** keys or values (unlike `HashMap`), and its iterators do not throw `ConcurrentModificationException`. [[What thread-safe collections exist in Java]] is the broader list.

> [!warning] “I only `get` on other threads”
> The documented duty to lock is when **any** thread modifies structurally. Publishing a fully built `HashMap` and then only reading it from many threads is a different pattern (safe publication of a stable map). Mixing unsynchronized `put`/`resize` with `get` is the unsupported case. Do not treat fail-fast CME as a concurrency protocol.

> [!tip] Interview answer
> **`HashMap` is not thread-safe. Concurrent structural updates need an external lock or `Collections.synchronizedMap`. For a concurrent hash table use `ConcurrentHashMap` (no nulls). `Hashtable` is the legacy synchronized map. Fail-fast iterators are a bug detector, not a memory model.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**HashMap vs ConcurrentHashMap.**

HashMap: не потокобезопасен, допускает 1 null-ключ, null-значения. ConcurrentHashMap: потокобезопасен. Java 7 — Segment. Java 8+ — CAS + synchronized на головах бакетов (лучше параллелизм). null-ключи и null-значения ЗАПРЕЩЕНЫ. computeIfAbsent — атомарная «проверь и вставь».

**HashMap vs ConcurrentHashMap.**

HashMap не потокобезопасен. ConcurrentHashMap потокобезопасен: в Java 7 — Segment-блокировки, в Java 8+ — CAS + synchronized на головах бакетов.

**HashMap vs ConcurrentHashMap — ключевые различия.**

HashMap не потокобезопасен, допускает null-ключ/значение. ConcurrentHashMap потокобезопасен, не допускает null, в Java 7 использовал сегментную блокировку, в Java 8+ — CAS + synchronized на головах бакетов.

**HashMap vs ConcurrentHashMap.**

HashMap: не потокобезопасен, null-ключ. ConcurrentHashMap: Java 8+ CAS + synchronized на головах бакетов. null запрещён. computeIfAbsent атомарен.

**HashMap vs ConcurrentHashMap.**

HashMap: не потокобезопасен, допускает null-ключ. ConcurrentHashMap: Java 7 — Segment-блокировки, Java 8+ — CAS + synchronized на головах бакетов. null запрещён. computeIfAbsent — атомарная операция.
