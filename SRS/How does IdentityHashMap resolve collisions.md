<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #DSA/Algorithms/Hashing #Java/HashCodeEquals #SRS

# How does `IdentityHashMap` resolve collisions?

> [!abstract] Short answer
> **Linear probing (open addressing), not chaining.** Keys and values sit in one array: keys at even indexes, values at odd. A collision walks the next key slot (`index + 2`, wrapping). Slots match with `==` and `System.identityHashCode`, never the key’s `hashCode` / `equals`. `HashMap` uses chaining. Faster probing is an implementation note, not a reason to use this as a general-purpose map.

## Probe the interleaved table

The class javadoc: a simple linear-probe table in the Sedgewick/Knuth style. One `Object[]`: even indexes hold keys, odd hold values (better locality than two arrays). Empty key slots are `null` (a null *key* is stored as a sentinel). Expected constant-time `get`/`put` if identity hashes spread. [[How does IdentityHashMap decide whether two keys are the same]] [[Does IdentityHashMap use the hashCode method]]

Lookup hashes with `System.identityHashCode`, maps that to an **even** index, then:

1. If `table[i] == key` (after masking null), the value is `table[i + 1]`.
2. If `table[i] == null`, the key is absent (end of the probe run).
3. Else collision: `i = i + 2`, wrap to `0`.

`put` uses the same walk and writes the first empty even slot. Delete cannot leave a hole that would make a later probe stop early; the implementation rehashes the following run into the vacated slot.

```d2
direction: down
h: "identityHashCode → even i" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
hit: "table[i] == key ?" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
empty: "table[i] == null\nstop: miss" {
  width: 220
  height: 70
  style.fill: "#ffcdd2"
}
next: "i = i+2 (wrap)\nlinear probe" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}

h -> hit
hit -> empty: empty slot
hit -> next: other key
next -> hit
```

**Fig. 1.** Open addressing: the next collision lives in the same array, two slots on. `HashMap` would append a node in that bucket.

```java
// Conceptual: IdentityHashMap table length is always even.
// hash() uses identityHashCode and lands on an even index.
Object[] table = /* keys at 0,2,4,… values at 1,3,5,… */;
Object k = /* lookup key, null masked */;
int i = /* hash(k, table.length) */;
for (;;) {
    Object item = table[i];
    if (item == k) { /* hit: value is table[i + 1] */ break; }
    if (item == null) { /* miss */ break; }
    i = (i + 2 < table.length) ? i + 2 : 0; // nextKeyIndex
}
```

**Listing 1.** Conceptual linear probe from OpenJDK `jdk-21-ga` (`hash` / `nextKeyIndex`). Not a compilable copy of the class.

`HashMap` is the chaining contrast in that same implementation note: collide in a bucket, then walk the chain. “Open addressing like HashMap” is the wrong pairing. [[What is the internal structure of HashMap]] [[When does a hashCode collision occur in a HashMap]] [[Why can IdentityHashMap be faster than HashMap]]

The javadoc’s “often faster than `HashMap`” is for many JREs and operation mixes, not a guarantee, and not a license to drop `equals` for ordinary keys. [[Does IdentityHashMap violate the Map contract]]

> [!warning] “Same hashtable as HashMap, just == instead of equals”
> Collision *strategy* differs: probe vs chain. Deleting in a probe table is not “clear the node and leave a gap.” Capacity is expected maximum size, not HashMap’s load-factor pair. Clustered identity hashes still degrade to long probe runs.

> [!tip] Interview answer
> **`IdentityHashMap` resolves collisions by linear probing in one interleaved key/value array.** It hashes with `System.identityHashCode` and compares with `==`. `HashMap` uses chaining. That can be faster, but the class is still not a general-purpose `Map`.
