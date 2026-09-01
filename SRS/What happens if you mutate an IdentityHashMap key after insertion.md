<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# What happens if you mutate an `IdentityHashMap` key after insertion?

> [!abstract] Short answer
> **Lookup with that same instance still hits.** After `put`, `get` and `containsKey` succeed if and only if the argument is **`==` the stored key**. Changing fields (even ones used by `equals`/`hashCode`) does not change identity or `System.identityHashCode`, so the entry stays in the same identity bucket. The same mutation on a `HashMap` key typically **loses** the mapping.

## After `put`, identity is the only key state that matters

`IdentityHashMap.get` returns the value for a stored key `k` such that `(key == k)`. `containsKey` is the same test. Buckets use `System.identityHashCode`, which is the default identity hash even when the class overrides `hashCode`. Field writes do not retarget `==` and do not rehash the identity code, so the table does not need to move the entry.

The general `Map` warning (behavior unspecified if you change a key in a way that **affects `equals` comparisons**) is the `HashMap` failure mode. This class intentionally does **not** compare keys with `equals`. [[Must IdentityHashMap keys be immutable]] is the policy form of that fact.

```text
put(key, v)           store that reference
key.field = newValue  same object, new equals/hashCode
ident.get(key)        hit   — key == stored key
ident.containsKey(key) hit
hash.get(key)         miss typical — current hashCode / equals
ident.get(copy)       miss  — copy != key even if equals
```

**Listing 1.** Same instance after mutation versus a value-equal copy. [[How does IdentityHashMap decide whether two keys are the same]]

```d2
direction: down
put: "put(k, v)\nk still the same object" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mut: "Mutate k's fields" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
ihm: "IdentityHashMap\nget(k) hits\nget(equalCopy) misses" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
hm: "HashMap\nget(k) typically misses" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

put -> mut
mut -> ihm
mut -> hm
```

**Fig. 1.** Mutation after insert: identity lookup still uses the original reference; value hashing does not.

```java
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Map;

final class MutableId {
    int id;
    MutableId(int id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof MutableId)) {
            return false;
        }
        return id == ((MutableId) o).id;
    }

    @Override
    public int hashCode() {
        return id;
    }
}

MutableId k = new MutableId(1);
Map<MutableId, String> ident = new IdentityHashMap<>();
Map<MutableId, String> hash = new HashMap<>();
ident.put(k, "v");
hash.put(k, "v");

k.id = 2;

ident.get(k);              // "v"
ident.containsKey(k);      // true
hash.get(k);               // typically null — unspecified Map behavior
ident.get(new MutableId(2)); // null
```

**Listing 2.** Conceptual: mutate after both `put`s. `IdentityHashMap` still finds `k`; `HashMap` usually does not. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is the equals-map case. [[Does IdentityHashMap use the hashCode method]] is why the identity bucket does not move.

A `null` key cannot be mutated. Replacing the variable with a new object is not this cue: that is a different `==` and a miss.

> [!warning] A quiet `equals` log is not extra magic
> Samples that print inside `equals`/`hashCode` stay silent on the `IdentityHashMap` path because lookup never calls those methods. That is the documented `==` / `identityHashCode` rule, not a quirk of one demo. It is also not permission to mutate keys you still store in a `HashMap`.

> [!tip] Interview answer
> **The entry stays findable with the same reference.** `IdentityHashMap` compares with `==` and hashes with `identityHashCode`, so mutating fields after `put` does not hide the mapping. A new object that would `equals` the key still misses. Do the same mutation in `HashMap` and lookup is typically lost.
