<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# How do you search for an element in an `ArrayList`?

> [!abstract] Short answer
> Use `contains` for yes/no, `indexOf` / `lastIndexOf` for the first or last index (`-1` if missing). All three compare with `Objects.equals`. That is a **linear** scan, not a hash lookup. `Collections.binarySearch` is O(log n) only on a **sorted** random-access list.

## Scan by `equals`, or binary-search a sorted list

```d2
direction: down
ask: "Need the element?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
has: "contains(o)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
idx: "indexOf / lastIndexOf" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
bin: "Collections.binarySearch\nlist must already be sorted" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

ask -> has
ask -> idx
ask -> bin
```

**Fig. 1.** Unsorted `ArrayList`: linear `equals` scan. Binary search is a different contract.

`contains(Object)` is true iff some element `e` satisfies `Objects.equals(o, e)`. `indexOf` returns the **lowest** such index, `lastIndexOf` the **highest**, or `-1`. OpenJDK implements `contains` as `indexOf(o) >= 0` and walks `elementData` from `0` to `size` (nulls with `==`, otherwise `o.equals`). The class specification puts this in the linear-time bucket (`get`/`set` are the constant-time indexed ops; end `add` is amortized constant) ([[What is the time complexity of searching in an ArrayList]]).

`hashCode` is not consulted. Two objects that would collide in a `HashSet` still compare only through `equals` here ([[Why should equals and hashCode be overridden together]]).

```java
List<String> names = new ArrayList<>(Arrays.asList("Ada", "Grace", "Ada"));

names.contains("Grace");     // true
names.indexOf("Ada");        // 0
names.lastIndexOf("Ada");    // 2
names.indexOf("Linus");     // -1

Collections.sort(names);
int i = Collections.binarySearch(names, "Grace"); // >= 0 if found
```

**Listing 1.** Membership vs first/last index. `binarySearch` requires ascending order first; if the list is unsorted, the result is **undefined**. Duplicate keys: which match is found is unspecified. On a random-access list (`ArrayList` `get` is constant time) it is O(log n) comparisons.

A loop with `get(i)` is the same linear scan. `list.stream().anyMatch(o::equals)` is also linear. For many independent lookups, copy into a `HashSet` ([[How do you convert an ArrayList to a HashSet in one line]]) — that is a different structure, not `ArrayList.contains`.

> [!warning] `contains` does not sort and does not hash
> Expect O(n) worst case even when the element exists ([[What is the worst case time complexity of contains on an ArrayList when the element exists]]). `binarySearch` on an unsorted `ArrayList` is not a faster `contains` — the API leaves that undefined (you can miss a present element).

> [!warning] `indexOf` returning `0` is a hit
> Only `-1` means absent. `if (list.indexOf(x) != 0)` is the wrong test (`x` at index 0 looks missing). `boolean` membership is `contains` or `indexOf(x) >= 0`.

> [!tip] Interview answer
> **`contains` or `indexOf` — linear `equals` from the front.** `lastIndexOf` searches from the back. `ArrayList` is not a hash table. Use `Collections.binarySearch` only after sorting, or a `Set` if you need expected-constant membership.
