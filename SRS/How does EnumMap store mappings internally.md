<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS

# How does `EnumMap` store mappings internally?

> [!abstract] Short answer
> **As an array of values, indexed by the key’s `ordinal()`.** The array length is the number of constants of that one enum type. There is no key `hashCode`, no bucket chain, and no collision list. A slot holds a value, a private sentinel for “mapped to `null`,” or `null` meaning “no mapping.” Basic `get`/`put` are constant time.

## One slot per constant

The public contract already says enum maps are arrays, compact, and typically faster than `HashMap` for enum keys ([[Why prefer EnumMap when the keys are enum constants]]). JDK 21’s `EnumMap` keeps:

- `keyType` — the single enum class ([[Must EnumMap keys all come from the same enum type]])
- `keyUniverse` — all constants of that type (cached, shared)
- `vals` — `Object[keyUniverse.length]`; `vals[k.ordinal()]` is the mapping for `k`

`ordinal()` is declaration position, unique within the type ([[What does ordinal do on a Java enum]]). Two keys never share an index, so there is nothing to resolve with hashing.

```d2
direction: down
keys: "Color.RED=0  GREEN=1  BLUE=2" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
vals: "vals[]  [ v0 | v1 | empty ]" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
idx: "index = key.ordinal()" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

keys -> idx -> vals
```

**Fig. 1.** Universe size is fixed when the map is created. `size()` counts filled slots, not `vals.length`.

```java
public V put(K key, V value) {
    typeCheck(key);
    int index = key.ordinal();
    Object oldValue = vals[index];
    vals[index] = maskNull(value);
    if (oldValue == null)
        size++;
    return unmaskNull(oldValue);
}
```

**Listing 1.** `put` in `java.util.EnumMap` (JDK 21). `get` is `vals[key.ordinal()]` after a type check. Neither calls `hashCode` on the key.

`maskNull` / `unmaskNull` are private. User `null` values are stored as a distinguished non-null sentinel so a slot can mean three things: empty, mapped to a value, mapped to `null`. That is why `get` returning `null` is ambiguous and `containsKey` tests `vals[index] != null` (the slot, not the user’s value). Null **keys** are still forbidden ([[Does EnumSet allow null]] is the set analogue; `EnumMap` matches on keys).

Constant-specific class bodies do not break indexing: `typeCheck` accepts `key.getClass() == keyType` **or** `key.getClass().getSuperclass() == keyType`, then still uses `ordinal()` of the enum constant.

## Not `HashMap`

`HashMap` spreads keys with `hashCode` and handles collisions in buckets. `EnumMap` never does that for lookup. “Collision probability is zero” is the wrong picture: collisions are not improbable; **the index is the identity of the constant**. A key from a different enum does not hash into a wrong bucket — `put` throws `ClassCastException`, `get` treats it as absent.

Views iterate `vals` from `0` to `length-1` and skip empty slots, which is why iteration is declaration order.

> [!warning] `maskNull` is not an API
> You cannot call it. It only exists so a stored `null` value is distinguishable from “no entry.” Prefer `containsKey` when `null` values are possible.

> [!warning] Array length is the enum, not `size()`
> `new EnumMap<>(Color.class)` allocates three slots for `{RED, GREEN, BLUE}` even while empty. Memory scales with how many constants the type has, not with how many mappings you inserted.

> [!tip] Interview answer
> **`EnumMap` is an array of values indexed by `ordinal()` — no hashing, no collision lists.** Empty slots are `null`; a real `null` value is masked with a sentinel. That is why operations are O(1) and why keys must all be the same enum type.
