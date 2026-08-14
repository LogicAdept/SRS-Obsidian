<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# Can a `HashMap` contain two equal keys at the same time?

> [!abstract] Short answer
> **No.** A `HashMap` cannot contain two keys that are equal according to its key-equality semantics. If you `put` an equal key, the existing mapping is replaced rather than a second mapping being added.

## What happens during `put`

A `HashMap` uses the key's hash to find a candidate bucket, then distinguishes the existing key from a new key using equality. Conceptually, the lookup is:

```d2
direction: down
hash: "1. Compute key.hashCode()" {
  width: 260
  height: 80
}
bucket: "2. Find candidate bucket" {
  width: 260
  height: 80
}
candidate: "3. Existing key found?" {
  width: 260
  height: 80
}
equal: "key == existingKey OR key.equals(existingKey)?" {
  width: 320
  height: 90
}
newEntry: "Not equal → add a new mapping" {
  width: 280
  height: 80
}
replace: "Equal → replace the value" {
  width: 280
  height: 80
}

hash -> bucket
bucket -> candidate
candidate -> equal: yes
candidate -> newEntry: no
equal -> replace: yes
equal -> newEntry: no
```

**Fig. 1.** A second key that is equal to an existing key does not create another mapping; the existing mapping is updated.

The `Map` contract defines a map as containing no duplicate keys: each key can map to at most one value. `HashMap.put` therefore replaces the old value when the map already contains a mapping for that key.

```java
record Key(int id) {}

Map<Key, String> map = new HashMap<>();

Key first = new Key(42);
Key second = new Key(42);

map.put(first, "A");
map.put(second, "B");

System.out.println(map.size());          // 1
System.out.println(map.get(first));      // B
System.out.println(map.get(second));     // B
```

**Listing 1.** `first` and `second` are distinct objects, but they are equal because the record's `equals` compares the same component value. The second `put` replaces the value of the existing mapping.

## Why `hashCode` matters

Equal keys must have the same `hashCode`. `HashMap` can use the hash to narrow the search before performing equality checks; Java's `Map` specification explicitly allows implementations to avoid `equals` when hash codes differ.

So the effective contract is:

```text
equal keys
    ↓
same hashCode
    ↓
same candidate bucket
    ↓
equality match
    ↓
existing mapping is reused
```

**Fig. 2.** Equal keys must agree on `hashCode`, allowing a hash table implementation to locate the relevant bucket before checking equality.

See [[How does HashMap use hashCode and equals]] and [[What happens when a mutable key is changed after insertion into HashMap]].

> [!warning] Different keys can still share a bucket
> A hash collision does **not** mean two keys are equal. Two unequal keys may have the same hash code and therefore land in the same bucket; `HashMap` still needs equality checks to distinguish them. The reverse is the important contract: if two keys are equal, their hash codes must be equal.

## The subtle implementation detail

When an equal but distinct key is inserted, the important observable rule is that the mapping is replaced and the map size does not grow. Do not describe this as "HashMap stores two equal keys but only returns one": the `Map` abstraction itself says there can be at most one mapping for an equal key.

> [!tip] Interview answer
> **No. A `HashMap` cannot contain two equal keys as two separate mappings. When you `put` an equal key, `HashMap` finds the existing mapping and replaces its value, so the size stays the same. Equal keys must also have the same `hashCode`, while unequal keys are still allowed to collide in one bucket.**

## NOTES

- Oracle Java SE 26 `Map` API: duplicate-key rule, `Objects.equals` key semantics, and the allowance for hash-based `equals` optimizations.
- Oracle Java SE 26 `HashMap` API: `put` replaces the old value when a mapping for the key already exists.
- Oracle Java SE 26 `Object` API: `equals`/`hashCode` contract requiring equal objects to have equal hash codes.
