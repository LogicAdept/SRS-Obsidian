<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is the worst-case time complexity of `add` on an `ArrayList`?

> [!abstract] Short answer
> **O(n).** End `add(E)` is O(n) when the backing array must grow (copy every live slot). Typical append is only **amortized** O(1). `add(index, e)` is O(n) even with spare capacity, because of the tail shift.

## One expensive grow, or a shift

```d2
direction: down
add: "add" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
end: "add(e) append" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
idx: "add(i, e)" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
grow: "full → copy n slots\nworst O(n)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
shift: "arraycopy tail\nO(n) even if not full" {
  width: 260
  height: 55
  style.fill: "#ffe0b2"
}

add -> end
add -> idx
end -> grow
idx -> shift
```

**Fig. 1.** Worst case depends which `add` ([[Does ArrayList always add elements in O(1) time]], [[How much extra memory can ArrayList add trigger when resizing]]).

The specification: `get`/`set` are constant time; **`add` runs in amortized constant time** — “adding n elements requires O(n) time.” That is the **total** for *n* end inserts, not a O(1) ceiling on one call. When `size == capacity`, OpenJDK `grow` uses `Arrays.copyOf`; that single `add(E)` is linear in the old length. The growth factor is **unspecified** in the API (~1.5× in OpenJDK).

`add(int index, E)` “shifts the element currently at that position (if any) and any subsequent elements to the right.” That is already linear. If the array is also full, you pay grow **plus** the shift. `addFirst` is `add(0, e)`.

```java
List<Integer> list = new ArrayList<>(1);
list.add(0);    // fits
list.add(1);    // worst-case append: copy, then store
list.add(0, -1); // worst-case indexed: shift (and grow if full)
```

**Listing 1.** Conceptual. Amortized append: [[What is the time complexity of appending to an ArrayList]]. How the array grows: [[How does resize ArrayList]].

> [!warning] “`add` is O(1)” is the amortized story
> Interviewers who ask for **worst** time want the grow (or the indexed shift). *n* appends still cost O(n) overall.

> [!warning] Name the overload
> `add(E)` worst case = resize. `add(i, e)` worst case = shift, with or without resize. One Big-O for both is incomplete.

> [!tip] Interview answer
> **Worst case O(n): a full `ArrayList` copies the backing array on that `add`.** End `add` is amortized O(1). Indexed `add` is O(n) because of the tail shift, even when capacity is already enough.
