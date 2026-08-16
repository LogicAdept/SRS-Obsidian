<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/WeakHashMap #Java/JVM/Memory #Java/HashCodeEquals #Java/Versions/8 #SRS

# What is the difference between `HashMap` and `WeakHashMap`?

> [!abstract] Short answer
> **`HashMap` strongly holds keys (and values). `WeakHashMap` holds keys only weakly, so the GC can drop a mapping when the key is otherwise unused.** Both are unsynchronized hash tables, allow a `null` key and `null` values, and document similar lookup cost if hashes spread. `WeakHashMap` therefore breaks familiar `Map` invariants: `size`, `containsKey`, and `get` can change with no mutator. It is not a drop-in `HashMap`.

## Same table shape, different reachability

```text
                 HashMap                         WeakHashMap
keys             strong                          weak (WeakReference)
values           strong                          strong
null key/value   yes                             yes
synchronized     no                              no
lookup           equals + hashCode               equals + hashCode
get/put cost     expected O(1) if hashes spread  similar to HashMap
size()           stable until you mutate         snapshot; may shrink
Java 8+ trees    yes (JEP 180)                   no
```

**Listing 1.** Class javadocs (Java SE 21) plus JEP 180’s explicit skip of `WeakHashMap`. [[What is WeakHashMap used for]] is when you want the weak-key behavior. [[What is the internal structure of HashMap]] is the strong-key table.

```d2
direction: down
k: "Key object" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
hm: "HashMap\nstrong key ref\nkey cannot be GC'd" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
wh: "WeakHashMap\nweak key ref\nGC may drop the entry" {
  width: 300
  height: 80
  style.fill: "#ffe0b2"
}

hm -> k
wh -> k
```

**Fig. 1.** If the map is the last ordinary reference, `HashMap` keeps the key; `WeakHashMap` does not.

`WeakHashMap` javadoc: it behaves as if an unknown thread were silently removing entries. Even after you synchronize and call no mutators, `size` can fall, `isEmpty` can flip, `containsKey` can go true then false, `get` can return a value then `null`. `HashMap` does not do that. `WeakHashMap.size()` is documented as a snapshot that may still include entries not yet expunged.

Both permit nulls and use `equals`/`hashCode` for lookup. `WeakHashMap` is **intended** for identity-`equals` keys; recreatable keys such as `String` make GC removal look like a random miss. That is a usage warning, not a different `get` contract. [[What is the difference between HashMap and IdentityHashMap]] is the map that actually compares with `==`.

## Values and eviction policy

`WeakHashMap` values stay **strong**. A value that points at its key (or a cycle through other entries) pins the key, so the “weak map” never drops that row. `HashMap` always pins both sides.

Neither is LRU. `LinkedHashMap.removeEldestEntry` evicts on insert/size. `WeakHashMap` evicts when the key is unreachable. [[How do you build a cache with invalidation using LinkedHashMap]] is the size hook.

> [!warning] `new WeakHashMap<>(hashMap)` is not “the same map, weaker”
> You copy mappings, then lose any key the rest of the program does not retain. Iterators are still fail-fast, but GC removal is a structural change you did not call. Do not use `WeakHashMap` as a general `HashMap` to “save memory” for `String` keys.

> [!tip] Interview answer
> **`HashMap` keeps strong refs to keys, so entries stay until you remove them. `WeakHashMap` keeps weak key refs, so the GC can delete mappings; `size`/`get`/`containsKey` are not stable. Values are strong in both. Same nulls, same unsynchronized hash table, similar expected lookup. Use `WeakHashMap` only when the map must not pin the key.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чем разница между `HashMap` и `WeakHashMap`? Для чего используется `WeakHashMap`?**

В Java существует 4 типа ссылок: _сильные (strong reference)_, _мягкие (SoftReference)_, _слабые (WeakReference)_ и _фантомные (PhantomReference)_. Особенности каждого типа ссылок связаны с работой Garbage Collector. Если объект можно достичь только с помощью цепочки WeakReference (то есть на него отсутствуют сильные и мягкие ссылки), то данный объект будет помечен на удаление.

`WeakHashMap` - это структура данных, реализующая интерфейс `Mindmap` и основанная на использовании WeakReference для хранения ключей. Таким образом, пара «ключ-значение» будет удалена из `WeakHashMap`, если на объект-ключ более не имеется сильных ссылок.

В качестве примера использования такой структуры данных можно привести следующую ситуацию: допустим имеются объекты, которые необходимо расширить дополнительной информацией, при этом изменение класса этих объектов нежелательно либо невозможно. В этом случае добавляем каждый объект в `WeakHashMap` в качестве ключа, а в качестве значения - нужную информацию. Таким образом, пока на объект имеется сильная ссылка (либо мягкая), можно проверять хэш-таблицу и извлекать информацию. Как только объект будет удален, то WeakReference для этого ключа будет помещен в ReferenceQueue и затем соответствующая запись для этой слабой ссылки будет удалена из `WeakHashMap`.
