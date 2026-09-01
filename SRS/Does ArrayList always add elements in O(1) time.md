<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# Does `ArrayList` always add elements in O(1) time?

> [!abstract] Short answer
> **No.** End `add` is **amortized** constant time: adding *n* elements is O(n). A single `add` that overflows capacity copies the backing array (linear in the old capacity). `add(index, e)` still shifts tail elements, so it is linear even when capacity is already enough.

## Amortized append, linear resize, linear insert

```d2
direction: down
add: "add(e) at the end" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
fit: "size < capacity\nstore at elementData[size]" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
grow: "size == capacity\ncopy to a larger array, then store" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

add -> fit: "usual case"
add -> grow: "overflow"
```

**Fig. 1.** Most appends write one slot. Overflow pays for a copy so later appends stay cheap on average.

The `ArrayList` specification: `get` / `set` run in constant time; **`add` runs in amortized constant time** — “adding n elements requires O(n) time.” Capacity grows automatically; **the growth policy is unspecified** beyond that amortized cost. `ensureCapacity` (or `new ArrayList<>(expectedSize)`) reduces how often reallocation happens ([[What is the difference between an array and an ArrayList]]).

OpenJDK’s `add(E)` stores at `elementData[size]` when there is a free slot. When `size == elementData.length` it calls `grow()`, which `Arrays.copyOf`s the buffer. Preferred extra length is `oldCapacity >> 1` (about 1.5×). That factor is an implementation choice, not an API guarantee. The no-arg constructor uses a shared empty array and expands to default capacity **10** on the first real element.

```java
List<Integer> list = new ArrayList<>(2); // capacity hint, size == 0
list.add(1); // O(1): write into existing slots
list.add(2);
list.add(3); // overflow: copy 2 slots, then store — this call is O(capacity)

list.add(0, 0); // shifts every element right — O(size), even with spare capacity
```

**Listing 1.** Conceptual costs for Java SE 21 / OpenJDK: append vs grow vs `add(int, E)`. `addFirst` is the same shift-from-zero case.

`add(int index, E)` “shifts the element currently at that position (if any) and any subsequent elements to the right.” That is the linear family (“all of the other operations run in linear time”), not the amortized-constant end `add`. Worst-case end `add` is the grow copy ([[What is the worst case time complexity of add on an ArrayList]]; growth mechanics: [[How does resize ArrayList]]).

> [!warning] “`add` is always O(1)” is false in two different ways
> (1) The spec already says **amortized** O(1) for `add`, not every call. (2) `add(index, e)` / `addFirst` copy a slice of the list even when no grow happens. Measuring one `add` in a tight loop can look O(1) until a resize spike.

> [!warning] Do not quote 1.5× as the contract
> The API refuses to specify how much capacity jumps. OpenJDK currently prefers 50% growth; another JDK may differ so long as end `add` stays amortized constant time.

> [!tip] Interview answer
> **No. Append is amortized O(1): n adds cost O(n), but a resize copies the whole backing array. Insert at an index is O(n) because of the shift. Call `ensureCapacity` or pass an expected size if you know n up front.**
