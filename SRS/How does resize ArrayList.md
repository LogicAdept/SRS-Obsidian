<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# How does `ArrayList` resize?

> [!abstract] Short answer
> When `add` needs more room than **capacity**, `ArrayList` allocates a **new** backing array and copies the old one. The public spec only promises **amortized constant-time** `add`; it does **not** freeze the growth factor. OpenJDK’s preferred jump is `oldCapacity + (oldCapacity >> 1)` (about 1.5×) via `Arrays.copyOf`.

## Overflow → new array → copy

```d2
direction: down
full: "size == elementData.length" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
grow: "grow(minCapacity)\npreferred +50% (OpenJDK)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
copy: "Arrays.copyOf(old, newCapacity)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

full -> grow -> copy
```

**Fig. 1.** Resize is a **copy**, not an in-place stretch. JLS arrays have a fixed `length` ([[What is the difference between an array and an ArrayList]]).

The class javadoc: capacity is the backing array’s length, always ≥ `size()`. It “grows automatically”; **details of the growth policy are not specified** beyond amortized-constant `add`. `ensureCapacity(minCapacity)` can grow **before** a burst of inserts. `trimToSize()` is the opposite direction ([[How does removing elements from an ArrayList work and how does size change]]).

OpenJDK `add(E)` calls `grow()` when `size == elementData.length`. `grow` asks `ArraysSupport.newLength(oldCapacity, minGrowth, oldCapacity >> 1)` then `elementData = Arrays.copyOf(elementData, newCapacity)`. `Arrays.copyOf` allocates a new array of that length and copies; extra slots are `null`.

The no-arg constructor does **not** start at capacity 10 in memory: it shares `DEFAULTCAPACITY_EMPTY_ELEMENTDATA`. The **first** `add` inflates to `DEFAULT_CAPACITY` (10), not 1.5× of zero. `new ArrayList<>(0)` uses a different empty sentinel (`EMPTY_ELEMENTDATA`) and grows from 0 with the normal formula. `new ArrayList<>(n)` (`n > 0`) starts at that length.

```java
ArrayList<Integer> list = new ArrayList<>(2);
list.add(1);
list.add(2); // still fits
list.add(3); // grow: copy 2 elements into a larger array, then store 3
```

**Listing 1.** Conceptual OpenJDK costs: the overflowing `add` is O(old capacity). Amortized over many appends: [[Does ArrayList always add elements in O(1) time]]. Extra memory on that copy: [[How much extra memory can ArrayList add trigger when resizing]].

`Vector` documents a different rule: if `capacityIncrement <= 0`, capacity **doubles**. Do not quote Vector’s doubling as `ArrayList`’s contract.

> [!warning] “Always 1.5×” is not in the JavaDoc
> Interview dumps often freeze 1.5. The API refuses to specify the factor. OpenJDK currently prefers 50% more (`oldCapacity >> 1`); another implementation may differ so long as `add` stays amortized O(1). The first grow from `new ArrayList()` is **to 10**, not to 1.

> [!warning] Resize copies; it does not mutate `length`
> An `Object[]` cannot grow. The list **replaces** `elementData` with a new array. Old buffer becomes garbage after the copy. A resize is O(n) data movement, which is why end `add` is amortized, not worst-case, O(1).

> [!tip] Interview answer
> **On overflow, allocate a larger `Object[]` and `copyOf` the old contents.** Spec: amortized O(1) `add`, growth factor unspecified. OpenJDK: about 1.5×, first default-list insert goes to 10. Call `ensureCapacity` if you know the final size.
