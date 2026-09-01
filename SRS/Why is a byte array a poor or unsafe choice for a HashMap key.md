<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Arrays #Java/HashCodeEquals #Java/Immutability #SRS

# Why is a `byte[]` a poor or unsafe choice for a `HashMap` key?

> [!abstract] Short answer
> **Legal as `K`, poor as a content key.** `Map<byte[], V>` compiles (`byte[]` is a reference type; primitive `byte` is not a type argument). `HashMap` treats the array as an **identity**, not as a sequence of bytes. Array types inherit `Object.equals` / `Object.hashCode`, so two independently allocated arrays with the same contents are two keys. Content comparison lives on `Arrays.equals` / `Arrays.hashCode`, which `HashMap` never calls. Mutating the cells does **not** change that identity pair; it becomes the classic lost-mapping bug only if a wrapper hashes the live contents. [[What requirements apply to keys used in a HashMap]] [[Can a primitive value be used directly as a Map key in Java]]

## Poor: contents are not the key

JLS array members are `length`, `clone`, and everything inherited from `Object` except `clone`. There is no content `equals`. `Map` lookup uses `(k1==null ? k2==null : k1.equals(k2))` after `hashCode` picks a bin. For a `byte[]`, that is `==` and the identity hash. A later `new byte[] { … }` with the same bytes misses, even when `Arrays.equals` is true. [[How are hashCode and equals implemented in java.lang.Object]]

```java
byte[] a = { 1, 2 };
byte[] b = { 1, 2 };
map.put(a, "v");
map.get(a);                 // "v"  — same reference
map.get(b);                 // null — b.equals(a) is false
Arrays.equals(a, b);        // true — unused by HashMap
a.hashCode() == b.hashCode(); // usually false; identity hashes
```

**Listing 1.** Conceptual lookup. `HashMap` never consults `Arrays.equals` or `Arrays.hashCode`. Two `put`s of equal-content arrays make `size == 2`. The same identity rule applies to `int[]` and every other array type.

```d2
direction: down
put: "put(a, v)\na is a byte[]" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
getA: "get(a)\nsame reference" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
getB: "get(b)\nArrays.equals(a, b)\na != b" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
put -> getA: hit
put -> getB: miss
```

**Fig. 1.** The usual intent is “these bytes.” The table answers “this array object.”

You cannot override `equals` on an array type. A content key is a wrapper that copies the bytes and implements `equals` / `hashCode` with `Arrays.equals` / `Arrays.hashCode` (the javadoc pair: equal contents ⇒ equal hashes). `String` is the common immutable stand-in when the bytes are text. Wrapping with `ByteBuffer` is **not** that fix: `ByteBuffer.equals` / `hashCode` use **remaining** elements (`position` through `limit - 1`), and the `hashCode` javadoc says it is inadvisable to use buffers as hash-map keys unless contents will not change. [[Why is String a common choice for HashMap keys]]

## Unsafe: mutability is a different bug

Array length is fixed after creation; components are not. Assigning `a[i] = …` does **not** change `a.equals` or `a.hashCode()`, so a raw `byte[]` key is **not** the stored-hash miss described in [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]]. The mapping still resolves through the same reference; only the payload you thought was “the key” has changed.

The `Map` contract is unspecified if you change a key so that `equals` comparisons change. That hits as soon as `equals` / `hashCode` **read the cells**: a record or class that stores the caller’s array and delegates to `Arrays.hashCode`. Clone on construction and do not publish a mutable view. Shared aliases of a raw `byte[]` key are still a design smell: every holder can rewrite the bytes while the map keeps answering `get(a)`. [[Why are mutable keys such as byte arrays risky in a HashMap]]

> [!warning] “I’ll just call `Arrays.hashCode` before `put`”
> That integer is not stored as the map’s notion of equality. `HashMap` still calls `key.hashCode()` and `key.equals` on the array object. Hash the contents only inside a type that owns a copy. `ByteBuffer.wrap` is the same trap: content-dependent hash, mutable window. There is no `HashMap` ban on array keys; the failure is **content lookup**, not `put`. The hash is `Object.hashCode()`, not a specified “address assigned at `new`.”

> [!tip] Interview answer
> **Yes, `Map<byte[], V>` is legal — primitive `byte` is not. A `byte[]` key is identity: two equal-content arrays miss each other. `Arrays.equals` is not `equals`. Mutating cells does not lose a raw-array mapping; it does lose a content wrapper that hashes the live array. Copy into an immutable key, or use `String`. Do not treat `ByteBuffer` as a drop-in.**
