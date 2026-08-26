<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Iteration #SRS

# Are `EnumMap` iterators fail-fast?

> [!abstract] Short answer
> **No.** Collection-view iterators on `EnumMap` are **weakly consistent**: they **never** throw `ConcurrentModificationException`, and they may or may not reflect map changes made while iteration is in progress. That is the opposite of fail-fast iterators on `HashMap` / [[Are IdentityHashMap iterators fail-fast]].

## What the class contract says

```d2
direction: right
ff: "Fail-fast\nHashMap, IdentityHashMap\n→ ConcurrentModificationException" {
  width: 280
  height: 100
  style.fill: "#ffebee"
}
wc: "Weakly consistent\nEnumMap, ConcurrentHashMap\n→ never CME" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
ff -> wc: "EnumMap is here"
```

**Fig. 1.** “Fail-fast” means best-effort CME on structural change. `EnumMap` documents the other model.

The Java SE class javadoc (same text in OpenJDK):

* iterators from `keySet()`, `values()`, and `entrySet()` are **weakly consistent**;
* they will **never** throw `ConcurrentModificationException`;
* they **may or may not** show effects of concurrent (or overlapping) modifications during the walk.

Iteration order is still the enum’s **natural order** (declaration order of constants). Weak consistency does not scramble that rule; it only drops the fail-fast CME check.

```java
enum Color { RED, GREEN, BLUE }

EnumMap<Color, String> map = new EnumMap<>(Color.class);
map.put(Color.RED, "r");
map.put(Color.GREEN, "g");

Iterator<Color> it = map.keySet().iterator();
map.put(Color.BLUE, "b"); // structural change during iteration
while (it.hasNext()) {
    Color c = it.next(); // no ConcurrentModificationException
}
```

**Listing 1.** Typical single-thread mutation during iteration: no CME. Whether `BLUE` appears in this walk is not guaranteed by the “may or may not” clause.

## Same family as concurrent maps, not as `HashMap`

[[Are ConcurrentHashMap iterators fail-fast]] is also **no** — weakly consistent, never CME. Interview tables that label every non-`Hashtable` map “fail-fast” are wrong for `EnumMap` (and for `EnumSet`, which uses the same wording).

`EnumMap` is still **not synchronized**. Weakly consistent iterators are not a substitute for external locking when multiple threads mutate the map.

> [!warning] Dump mix-up: “fail-fast like ConcurrentHashMap”
> Some dumps call `EnumMap` iterators **fail-fast** and then say they do **not** throw CME and may miss mid-iteration updates. That second half is weakly consistent behavior. Fail-fast means the CME path used by `HashMap`, not “iterate without crashing.”

> [!tip] Interview answer
> **No — `EnumMap` view iterators are weakly consistent, not fail-fast.** They never throw `ConcurrentModificationException` and may or may not see puts/removes that happen during the walk. Order follows enum declaration order. Do not lump them with `HashMap`’s fail-fast iterators.
