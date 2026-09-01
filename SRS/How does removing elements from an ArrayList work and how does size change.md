<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# How does removing elements from an `ArrayList` work and how does size change?

> [!abstract] Short answer
> Each successful `remove` decreases **`size()` by one** and **slides later elements left** so indexes stay contiguous. The backing array’s **capacity is unchanged**. Automatic growth is for `add`; shrinking is `trimToSize()`.

## `size()` drops; the buffer does not

```d2
direction: down
s4: "size() = 4\n[w, x, y, z | spare…]" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
rm: "remove(index) or remove(Object)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
s3: "size() = 3\n[w, y, z, null | same spare]" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

s4 -> rm -> s3
```

**Fig. 1.** Logical length is `size()`. Capacity is `elementData.length` and is not part of the public `ArrayList` API ([[What is the difference between an array and an ArrayList]]).

`remove(int index)` removes that slot and “shifts any subsequent elements to the left (subtracts one from their indices).” Out-of-range indexes throw `IndexOutOfBoundsException`. `remove(Object)` removes the first `e` with `Objects.equals(o, e)` (first `null` if the argument is `null`) and returns whether the list changed. `removeFirst` / `removeLast` (Java 21) are the two ends.

OpenJDK funnels these through `fastRemove`: `System.arraycopy` of the tail when the hole is not the last slot, then `size = size - 1` and `elementData[size] = null` so the dropped reference can be collected. No smaller array is allocated. `clear()` nulls `0 .. oldSize-1` and sets `size` to 0; capacity stays.

```java
ArrayList<String> list = new ArrayList<>(8);
Collections.addAll(list, "w", "x", "y", "z");
list.size();           // 4

String gone = list.remove(1); // "x"; list is [w, y, z]
list.size();           // 3

list.remove("z");      // true; list is [w, y]
list.size();           // 2

list.trimToSize();    // capacity now equals size(); not implied by remove
```

**Listing 1.** `size()` tracks live elements. `trimToSize()` is the shrink; `add` may `grow` later ([[Does ArrayList always add elements in O(1) time]], [[How does resize ArrayList]]).

Middle `remove` is linear in the tail (the spec’s non-constant operations). Removing the last index skips the copy.

> [!warning] `size()` after `remove` is not “the array got smaller”
> `size()` is the element count. Memory for the buffer stays until `trimToSize()`. There is no public `capacity()` on `ArrayList` (unlike `Vector`).

> [!warning] `remove(1)` on `List<Integer>` is an index
> Overload resolution picks `remove(int)`, not “value 1”. Use `remove(Integer.valueOf(1))` for the first `Integer` equal to 1.

> [!tip] Interview answer
> **`remove` decrements `size()` and compact-shifts to the left. Capacity does not auto-shrink — call `trimToSize()` if you care about the extra array. `add` is what grows the buffer.**
