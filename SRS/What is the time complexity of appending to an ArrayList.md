<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is the time complexity of appending to an `ArrayList`?

> [!abstract] Short answer
> **Amortized O(1)** for end `add` (`add(E)` / `addLast`): adding *n* elements is O(n). A single append that fills the backing array copies it, so **that call is O(n)**. Indexed `add(index, e)` is not append — it is O(n) because of the tail shift.

## Write one slot, or copy the array first

```d2
direction: down
app: "append add(e)" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
ok: "size < capacity\nO(1)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
copy: "size == capacity\ngrow + copy → O(n)" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}

app -> ok
app -> copy
```

**Fig. 1.** Append cost is amortized over later cheap writes ([[Does ArrayList always add elements in O(1) time]], [[How does resize ArrayList]]).

The `ArrayList` specification: `get`/`set` are constant time; **`add` runs in amortized constant time** — “adding n elements requires O(n) time.” That is the official bound for **end** `add`. Growth policy is **unspecified** beyond that amortized cost. OpenJDK copies with `Arrays.copyOf` and a preferred extra of `oldCapacity >> 1` (~1.5×); do not quote 1.5× as the contract.

Empty `ArrayList()` uses a shared empty buffer and expands to default capacity **10** on the first element. `new ArrayList<>(n)` / `ensureCapacity` cuts how often a grow happens; it does not change the amortized class.

```java
List<Integer> list = new ArrayList<>(2);
list.add(1); // append, fits — O(1)
list.add(2); // append, fits
list.add(3); // append, overflow — this call is O(capacity)

list.add(0, 0); // not append: shift — O(size)
```

**Listing 1.** Conceptual. Worst-case **one** `add(E)`: [[What is the worst case time complexity of add on an ArrayList]]. Peak memory on grow: [[How much extra memory can ArrayList add trigger when resizing]].

> [!warning] Amortized is not “every `add` is O(1)”
> A tight loop of appends is O(n) total with occasional linear spikes. Saying “append is O(1)” without **amortized** fails a worst-case follow-up.

> [!warning] `add(i, e)` is not appending
> `add(int, E)` “shifts … subsequent elements to the right.” Front/`addFirst` is the same linear family, even with spare capacity.

> [!tip] Interview answer
> **Appending is amortized O(1): n appends cost O(n).** One `add` that grows the array is O(n). Insert at an index is a different method and is O(n) because of the shift, not because of append.
