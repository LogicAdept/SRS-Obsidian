<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/Versions/9 #SRS

# Can you populate a `Map` from a collection of entries or key value pairs?

> [!abstract] Short answer
> **Yes — but not with `new HashMap<>(listOfEntries)`.** There is no `Map` / `HashMap` constructor that takes a `Collection` of entries. You copy from another **`Map`** (`putAll`, copy constructor), build from pairs (`Map.of`, `Map.ofEntries` + `Map.entry`, Java 9), snapshot with `Map.copyOf` (Java 10), or walk entries/`Collectors.toMap` yourself. Duplicate-key rules differ: mutable `put` replaces; factories throw.

## From a `Map`, not from a `Collection`

General-purpose maps document two constructors: empty, and `Map` copy. `HashMap(Map m)` copies mappings with default load 0.75 and capacity enough for `m`. `putAll(m)` is specified as `put(k, v)` once per mapping; later equal keys **replace**. `m == null` is `NullPointerException`. If `m` has a defined encounter order, `putAll` generally follows it. [[What is the Map interface in Java]] [[Can keys be duplicated in a Java Map]]

`Map` is not a `Collection`. There is no `addAll` of entries on the map itself. `entrySet()` is a view **out**, not a populate-in API.

```d2
direction: down
src: "What do you have?" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
map: "another Map\nputAll / copy ctor / copyOf" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
pairs: "k,v pairs or Entry…\nof / ofEntries / loop / toMap" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
no: "Collection<Entry> into HashMap(c)\nno such constructor" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}

src -> map
src -> pairs
src -> no
```

**Fig. 1.** Populate from a map or from pairs. A list of `Map.Entry` is not a `Map`.

## Pairs and `Entry` objects (Java 9+)

```java
Map<String, Integer> a = Map.of("x", 1, "y", 2);           // up to 10 pairs
Map<String, Integer> b = Map.ofEntries(
        Map.entry("x", 1),
        Map.entry("y", 2));
Map<String, Integer> c = Map.copyOf(b);                    // since 10
map.putAll(b);
Map<String, Integer> d = new HashMap<>(b);
```

**Listing 1.** Official factories and the two mutable copy paths. `ofEntries` extracts keys and values; it does **not** store the `Entry` objects. `Map.entry` entries are unmodifiable (`setValue` → `UnsupportedOperationException`), reject nulls, and are not serializable (`AbstractMap.SimpleEntry` if you need that).

Unmodifiable maps from `of` / `ofEntries` / `copyOf`: no null keys or values (`NullPointerException`); duplicate keys at creation → `IllegalArgumentException`; mutators → `UnsupportedOperationException`; iteration order unspecified. `copyOf` of an already unmodifiable map generally does not copy.

A `Collection<Map.Entry<K,V>>` still needs an explicit walk:

```java
Map<String, Integer> m = new HashMap<>();
for (Map.Entry<String, Integer> e : entries) {
    m.put(e.getKey(), e.getValue());
}
Map<String, Integer> s = entries.stream()
        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
```

**Listing 2.** There is no bulk `putAll(Collection<? extends Entry>)`. `Collectors.toMap` (no merge function) throws `IllegalStateException` on duplicate keys; pass a `BinaryOperator` to merge. Default map is a `HashMap`. `toUnmodifiableMap` exists since 10.

> [!warning] `new HashMap<>(entries)` does not compile
> The argument must be a `Map`, not a `List`/`Set` of pairs. `Map.of("a", 1, "a", 2)` fails fast; `putAll` of the same two mappings keeps the last value. `putAll` on an unmodifiable map throws `UnsupportedOperationException` (an empty source may skip the throw). Do not mutate the source map while `putAll` runs — that case is undefined.

> [!tip] Interview answer
> **Yes. Copy a `Map` with `putAll` or the copy constructor. For literals, `Map.of` (≤10 pairs) or `Map.ofEntries(Map.entry(k, v), …)` give an unmodifiable map (Java 9; `copyOf` in 10). A collection of entries is not a constructor argument — loop `put` or `Collectors.toMap`. Factories reject duplicate keys; `put`/`putAll` replace.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Почему Map отдельно от Collection?**

Collection хранит элементы — единичные значения. Map хранит ПАРЫ ключ-значение, у неё другой API: put(key, value), get(key), entrySet(). Хотя по сути обе — структуры данных.
