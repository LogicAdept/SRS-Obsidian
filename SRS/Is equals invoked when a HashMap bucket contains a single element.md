<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #Java/HashCodeEquals #SRS

# Is `equals` invoked when a HashMap bucket contains a single element?

> [!abstract] Short answer
> **Yes, it can be.** One node in the bucket does not skip equality. After `HashMap` computes the key’s hash and opens that bucket, it still compares the lookup key with the stored key: same reference first, then `equals`, unless the hashes already differ.

`HashSet` uses the same map internally, so [[How is HashSet implemented in terms of HashMap]] follows the same lookup.

## Lookup when `get` runs

```d2
direction: down
hash: "1. Mix key.hashCode()\ninto the stored hash" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
bucket: "2. Index the table\n(hash & (n - 1))" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
empty: "Bucket empty\n→ not found" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
node: "3. Inspect the first node\n(the only one, if size is 1)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
hashEq: "node.hash == hash?" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
noEq: "No equals()\n→ not found" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
id: "key == node.key?" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
foundId: "Found\n(equals() skipped)" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
eq: "key.equals(node.key)?" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
foundEq: "Found or miss\nfrom equals()" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}

hash -> bucket
bucket -> empty
bucket -> node
node -> hashEq
hashEq -> noEq: no
hashEq -> id: yes
id -> foundId: yes
id -> eq: no
```

**Fig. 1.** A one-node bucket still walks hash, then identity, then `equals`. The chain length does not drop those checks.

The first node is exactly the path `HashMap.getNode` takes when the chain has length one (a tree bin needs several nodes, so this case is an ordinary `Node`).

```java
map.get(key);
```

**Listing 1.** `get` is the usual cue; `containsKey` uses the same node search.

## One element is not a shortcut

Different keys can share a bucket even when their `hashCode` values differ: the index is only `hash & (n - 1)`. `HashMap` therefore compares the **stored hash** before it calls `equals`. See [[When does a hashCode collision occur in a HashMap]] and [[What is the internal structure of HashMap]].

```java
if (node.hash == hash &&
        (key == node.key || key.equals(node.key))) {
    return node; // found
}
```

**Listing 2.** Conceptual first-node test from `getNode` (Java 8+). `equals` runs only if the hashes match and the references differ.

> [!example] Two `Key` instances, one bucket
> Same `hashCode`, different objects. After the hash matches, `equals` runs and the value `"A"` is returned.

```java
record Key(int id) {}

Map<Key, String> map = new HashMap<>();
map.put(new Key(1), "A");
map.get(new Key(1));
```

**Listing 3.** Typical interview setup: two equal keys that are not the same reference.

> [!warning] Same reference skips `equals`
> If the lookup key **is** the stored key, identity succeeds and `equals` is not called. [[What is the difference between HashMap and IdentityHashMap]] is the map that **only** uses identity.

```java
Key key = new Key(1);
map.put(key, "A");
map.get(key); // key == node.key
```

**Listing 4.** Identity match: `equals` is skipped even though the bucket has one node.

> [!tip] Interview answer
> **A single element in the bucket does not mean `equals` is skipped.** `hashCode` chooses the bucket; then `HashMap` checks the stored hash, then `==`, then `equals` if the objects are not the same reference. `equals` is skipped when the hashes differ or when the keys are the same object.
