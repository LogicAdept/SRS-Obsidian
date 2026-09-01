<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Immutability #SRS

# What is the difference between `List.of(1, 2, 3)` and `new ArrayList()`?

> [!abstract] Short answer
> `List.of(1, 2, 3)` is a **three-element unmodifiable** list (Java 9): no add/remove/**replace**, no `null`, value-based. `new ArrayList<>()` is an **empty, resizable** `ArrayList` that permits `null`. They are not two spellings of `[1, 2, 3]`. `List.of` is not an `ArrayList`. Copy with `new ArrayList<>(List.of(1, 2, 3))` if you need both the literals and mutation.

## Frozen triple vs empty growable list

```d2
direction: right
of: "List.of(1, 2, 3)\nsize 3, UOE, no null" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
al: "new ArrayList<>()\nsize 0, add grows, nulls OK" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
copy: "new ArrayList<>(List.of(1, 2, 3))\nindependent mutable copy" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

of -> copy
```

**Fig. 1.** Same three numbers only after you **copy** the factory list into an `ArrayList`.

`List.of(E, E, E)` “returns an unmodifiable list containing three elements.” Unmodifiable lists: mutators **always** throw `UnsupportedOperationException`; `null` elements throw `NullPointerException` at creation; order follows the arguments; `RandomAccess`; **value-based** (do not sync on the instance; identity is unspecified). Nested mutable elements can still appear to change. The spec says **unmodifiable**, not “immutable.”

`ArrayList` “implements all optional list operations, and permits all elements, including `null`.” `ArrayList()` constructs an **empty** list (`size() == 0`); the default empty buffer inflates to capacity **ten** on the first `add`. End `add` is amortized constant time ([[Does ArrayList always add elements in O(1) time]]).

```java
List<Integer> of = List.of(1, 2, 3);
of.size(); // 3
// of.add(4);           // UnsupportedOperationException
// of.set(0, 9);        // UnsupportedOperationException
// List.of(1, null, 3); // NullPointerException

List<Integer> al = new ArrayList<>();
al.size(); // 0
al.add(1);
al.add(null);         // allowed

List<Integer> copy = new ArrayList<>(of);
copy.add(4);          // [1, 2, 3, 4]
```

**Listing 1.** `List.of` vs empty `ArrayList` vs copy-constructor. `Arrays.asList(1, 2, 3)` is a third thing: **fixed-size**, `set` writes through, not `java.util.ArrayList` ([[How do you convert a String array to an ArrayList]]). `List.copyOf(growable)` is the unmodifiable snapshot of a collection (rejects `null`s).

> [!warning] `new ArrayList()` is empty
> Interviewers who write `List.of(1, 2, 3)` vs `new ArrayList<>()` are asking factory **and** emptiness, not “two mutable lists.” `instanceof ArrayList` on `List.of(...)` is the wrong test (value-based, unspecified implementation).

> [!warning] Unmodifiable is not “deep freeze”
> `set` is rejected too, not only `add`/`remove`. Mutating an element object still shows through. `Collections.unmodifiableList(arrayList)` is a **view**: mutating `arrayList` still changes what the wrapper shows.

> [!tip] Interview answer
> **`List.of(1, 2, 3)` is a Java 9 unmodifiable three-element list: no nulls, no mutators, not an `ArrayList`.** `new ArrayList<>()` is empty and growable. If you need those three values and later `add`, copy: `new ArrayList<>(List.of(1, 2, 3))`.
