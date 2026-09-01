<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Map/HashMap #Java/Language/Enum #SRS

# What is the difference between `EnumMap` and `HashMap`?

> [!abstract] Short answer
> **Same `Map` API, different key universe and table.** `EnumMap` is a specialized map whose keys must all be constants of **one** enum type; it is an array indexed by `ordinal()`, iterated in declaration order. `HashMap` is the general hash table: any object key (including enums and one `null` key), unspecified order, buckets that can collide. You *may* put enum keys in a `HashMap`; `EnumMap` exists because that case has a denser, typically faster representation.

## Contract vs representation

Both implement `Map` (`get` / `put` / `putAll`). Both allow `null` **values**. Neither is synchronized. `EnumMap` arrived in 1.5; `HashMap` in 1.2.

`EnumMap` javadoc: all keys come from a single enum type specified when the map is created. Internally it is arrays, “extremely compact and efficient.” Views iterate in **natural order** — the order the constants are declared. `Enum.ordinal()` exists for structures like `EnumMap` / `EnumSet`; the map uses that index, not `hashCode`. [[How does EnumMap store mappings internally]] [[Must EnumMap keys all come from the same enum type]]

`HashMap` javadoc: hash-table `Map`, one `null` key, `null` values, **no** order guarantee, expected constant-time `get`/`put` if hashes spread. Collisions are a hash-table fact, not an `EnumMap` property. [[What is the internal structure of HashMap]] [[When does a hashCode collision occur in a HashMap]]

```text
                 EnumMap                            HashMap
keys             constants of one enum type         any object; one null key
null key         put throws NullPointerException    permitted
storage          Object[] slot per constant         buckets; hash then equals
index            key.ordinal()                      spread hashCode
order            declaration (natural) order        unspecified
basic ops        O(1); likely faster than HashMap   expected O(1)*
iterators        weakly consistent; never CME       fail-fast
construct        Class<K> (or a non-empty Map)      empty / capacity / Map
```

**Listing 1.** Java SE 21 class javadocs plus OpenJDK `EnumMap.put` (`vals[key.ordinal()]`). `*` assuming hashes disperse. “Likely faster” is the official implementation note, not a guarantee.

```d2
direction: down
need: "Keys are one enum type?" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
em: "EnumMap\narray[ordinal] = value" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
hm: "HashMap\nhash → bucket → equals" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

need -> em: yes
need -> hm: no, or mixed keys
```

**Fig. 1.** Choose `EnumMap` when the key *is* that enum. `HashMap` stays the general map, including maps that happen to use enum keys.

## Construction and lookup

An empty `EnumMap` needs the key type: `new EnumMap<>(Color.class)`. Copying another map with `new EnumMap<>(m)` works if `m` is already an `EnumMap`, or if `m` has **at least one** mapping so the key type can be inferred; an empty non-`EnumMap` throws `IllegalArgumentException`. `HashMap` has a true empty constructor and `HashMap(Map)` that only needs a non-null map. [[How do you create an EnumMap]]

```java
enum Color { RED, GREEN, BLUE }

EnumMap<Color, String> em = new EnumMap<>(Color.class);
em.put(Color.RED, "r");

Map<Color, String> hm = new HashMap<>();
hm.put(Color.RED, "r");
hm.put(null, "n"); // HashMap only

// em.put(null, "n");                 // NullPointerException
// new EnumMap<Color, String>(hm);    // NPE: HashMap has a null key
// new EnumMap<>(new HashMap<Color, String>()); // IAE: empty, not an EnumMap
```

**Listing 2.** Same enum keys in both maps. `put(null, …)` is legal on `HashMap` and rejected on `EnumMap`. `containsKey(null)` / `remove(null)` on `EnumMap` do **not** throw — they behave as a missing key.

OpenJDK `get`/`containsKey` check the runtime class then read `vals[ordinal]`. There is no bucket chain and no `hashCode` on that path. `put` type-checks the key (`ClassCastException` if it is the wrong enum type) then writes the same slot. `HashMap.get` matches with `equals` after hashing. For enum constants, `equals` is identity anyway; the win is skipping the hash table, not a different equality rule.

Iteration: `EnumMap` key/entry/value iterators follow declaration order and are **weakly consistent** (they never throw `ConcurrentModificationException`). `HashMap` view iterators are **fail-fast**. [[In what order does EnumMap iterate]] [[Are EnumMap iterators fail-fast]]

> [!warning] Enum keys in `HashMap` are legal — and “no collisions” is not a `HashMap` claim
> A `HashMap<Color, V>` compiles and runs. `EnumMap` is the specialized pick when every key is that enum, not a second `Map` type you *must* use. Do not say `EnumMap` is “`HashMap` without collisions.” Ordinal indexing means **one slot per constant**, so there is no hash-bucket collision; `HashMap` can still collide, including on enum keys. Speed is “likely, though not guaranteed.” Why that specialization exists: [[Why prefer EnumMap when the keys are enum constants]]. Null-key rules: [[Does EnumMap allow null keys or null values]].

> [!tip] Interview answer
> **`EnumMap` is a `Map` for one enum type: array indexed by `ordinal()`, declaration order, no null keys, likely faster than `HashMap` for that case. `HashMap` is the general hash table: any keys, one null key, unspecified order, possible collisions. You can put enums in a `HashMap`; use `EnumMap` when the key universe is that enum.**
