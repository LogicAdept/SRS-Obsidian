<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# How much extra memory can `ArrayList.add` trigger when resizing?

> [!abstract] Short answer
> On overflow OpenJDK allocates a **new** `Object[]` of length about **1.5×** old capacity (`old + (old >> 1)`), then copies. **Net** extra slots ≈ half the old capacity. **Peak** extra is the **whole new array while the old one is still live** (about 2.5× the old buffer in references). The JavaDoc does not specify the factor.

## Net growth vs peak during `copyOf`

```d2
direction: down
old: "old Object[]\ncapacity C" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
both: "copyOf allocates new\nlength ≈ C + C/2\nboth arrays live" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
done: "elementData points at new\nold array becomes garbage" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

old -> both -> done
```

**Fig. 1.** Extra heap is measured in **reference slots**, not a portable byte count. Peak is old + new; after GC, only the new buffer remains ([[How does resize ArrayList]]).

Public contract: `add` is amortized constant time; **growth policy is unspecified**. You cannot quote a byte figure from the API.

OpenJDK `grow` (when the list already has a real buffer) computes

`newCapacity = ArraysSupport.newLength(oldCapacity, minCapacity - oldCapacity, oldCapacity >> 1)`

then `elementData = Arrays.copyOf(elementData, newCapacity)`. `newLength` returns `old + max(minGrowth, prefGrowth)` when that stays ≤ `Integer.MAX_VALUE - 8` (`SOFT_MAX_ARRAY_LENGTH`). For a single overflowing `add`, min growth is 1 and preferred is `C/2`, so **new length is `C + C/2`**. `Arrays.copyOf` allocates an array of that length and copies; extra slots are `null`.

```java
ArrayList<Object> list = new ArrayList<>(8);
for (int i = 0; i < 8; i++) list.add(i);
list.add("overflow");
// OpenJDK: new Object[12], copy 8 refs; peak ≈ 8 + 12 slots, net +4 slots
```

**Listing 1.** Conceptual: capacity 8 → 12. Amortized cost of that copy: [[Does ArrayList always add elements in O(1) time]]. If the buffer already has a free slot, that `add` allocates **no** extra array.

Special cases: `new ArrayList()` shares an empty array; the **first** `add` allocates **10** slots (`DEFAULT_CAPACITY`), not 1.5× of 0. `new ArrayList<>(0)` grows with `newLength` from 0 (preferred growth 0), so the first grow can be **1** slot. Near `Integer.MAX_VALUE`, `newLength` clamps or throws `OutOfMemoryError`; allocation can still fail if the heap is short.

> [!warning] Peak is not “+50%”
> `copyOf` needs the **new** array before the old one can die. For capacity `C`, peak backing storage is about `C + 1.5C` references, then the old `C` can be collected. Saying “add uses 50% more memory” understates the spike.

> [!warning] Do not convert slots to megabytes
> Each slot is a reference; width depends on the JVM (compressed oops, headers, alignment). The spec never publishes a byte cost. Quote **slot counts** and “implementation-defined growth.”

> [!tip] Interview answer
> **On resize OpenJDK allocates ~1.5× the old `Object[]` and copies; net extra is about half the old capacity, but peak is both arrays at once.** The API does not fix the factor. Pre-size with `new ArrayList<>(n)` or `ensureCapacity` if you want to avoid that copy.
