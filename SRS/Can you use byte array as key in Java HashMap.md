<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Arrays #Java/HashCodeEquals #SRS

# Can you use a `byte[]` as a key in a Java `HashMap`?

> [!abstract] Short answer
> **Yes. Arrays are objects, and `HashMap` accepts any reference key (plus one `null`).** `Map<byte[], V>` compiles. Lookup uses the array’s inherited identity `equals` / `hashCode`, so `get` hits only with the **same instance**. A second array with the same bytes is a second key. That is legal, not a compile error. Whether it is a good key is [[Why is a byte array a poor or unsafe choice for a HashMap key]].

## It is a legal `K`

JLS: arrays are objects; every `Object` method except `clone` is inherited. `HashMap.put(K, V)` takes that reference. `byte[]` is a reference type, so it may appear as a generic argument. `byte` may not. [[Can a primitive value be used directly as a Map key in Java]]

```java
Map<byte[], String> map = new HashMap<>();
byte[] k1 = { 1, 2 };
map.put(k1, "v");
map.get(k1);                      // "v"
map.containsKey(k1);              // true
```

**Listing 1.** Same reference: `put` then `get` succeed. `HashMap` permits this key the same way it permits any other `Object`.

`put` replaces the value only when the new key `equals` an existing one. Two distinct arrays never `equals`, even when `Arrays.equals` is true, so a second `put` adds a second mapping.

```java
byte[] k1 = { 1, 2 };
byte[] k2 = { 1, 2 };
map.put(k1, "a");
map.put(k2, "b");
map.size();                       // 2
map.get(k1);                      // "a"
map.get(k2);                      // "b"
k1.hashCode() == k2.hashCode();   // usually false; identity hashes, not Arrays.hashCode
```

**Listing 2.** Same contents, two keys. `hashCode()` on the array is `Object.hashCode`, not `Arrays.hashCode(byte[])`. Unequal identity hashes are the usual case, not a uniqueness theorem.

```d2
direction: down
legal: "Map<byte[], V>\ncompiles, put stores the reference" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
same: "get(same array object)\nhit" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
copy: "get(new byte[]{ … })\nmiss, even if Arrays.equals" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
legal -> same
legal -> copy
```

**Fig. 1.** “Can you?” is yes. “Will a copy look up?” is no. The same identity rule applies to `int[]` and every other array type.

> [!warning] Interview “no, arrays are not keys”
> There is no `HashMap` ban on array keys. The failure mode is **content lookup**, not `put`. Mutating cells does not drop a raw-array mapping; that is [[Why are mutable keys such as byte arrays risky in a HashMap]].

> [!tip] Interview answer
> **Yes: `byte[]` is an object, `Map<byte[], V>` is legal, `put`/`get` work for that instance. Two equal-content arrays are two keys because array `equals` is `==`. Use it only if identity is what you want; otherwise wrap a copy or use `String`.**
