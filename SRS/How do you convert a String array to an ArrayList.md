<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Arrays #SRS

# How do you convert a `String` array to an `ArrayList`?

> [!abstract] Short answer
> Copy through `Arrays.asList` into `new ArrayList<>(…)`. That constructor walks the list and builds an independent, resizable `java.util.ArrayList`. `Arrays.asList` alone is a **fixed-size list view of the same array**, not an `ArrayList`.

## View first, then copy if you need `ArrayList`

```d2
direction: down
arr: "String[] words" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
view: "Arrays.asList(words)\nfixed-size List, same storage" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
copy: "new ArrayList<>(view)\njava.util.ArrayList, own backing array" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
arr -> view: "no copy"
view -> copy: "copy elements"
```

**Fig. 1.** `asList` wraps the array. `ArrayList(Collection)` copies into a real `ArrayList` that can grow ([[What is the difference between an array and an ArrayList]]).

`Arrays.asList(T... a)` returns a list **backed by** the specified array: `set` on the list writes through to the array, and array stores show up in the list. Size-changing optional operations (`add`, `remove`, `clear`, …) leave the list unchanged and throw `UnsupportedOperationException`. The list is `Serializable` and `RandomAccess`. A `null` array throws `NullPointerException`.

That list is **not** `java.util.ArrayList`. OpenJDK implements it as a private nested `Arrays.ArrayList` that holds a `final` reference to the same `E[]`. `java.util.ArrayList` is a separate resizable implementation that permits all optional list operations, including `null` elements.

To obtain that class, pass the view to the copy constructor: it constructs a list containing the collection’s elements in iterator order. The new list has its own backing store, so later `words[i] = …` does not change the `ArrayList`, and `list.add` does not change the array.

```java
String[] words = {"ace", "boom", "crew", "dog", "eon"};

List<String> view = Arrays.asList(words);          // not java.util.ArrayList
ArrayList<String> list = new ArrayList<>(view);  // independent copy
list.add("fox");
```

**Listing 1.** Idiomatic conversion: wrap, then copy. The same pattern works for any **reference** element type (`Integer[]`, …), not only `String[]`. Map views use the same constructor: [[How do you convert a HashMap to an ArrayList]].

Two other ways to fill a real `ArrayList` (Java SE 21):

```java
String[] words = {"ace", "boom", "crew", "dog", "eon"};

ArrayList<String> viaAddAll = new ArrayList<>();
Collections.addAll(viaAddAll, words); // varargs or array

ArrayList<String> viaStream = Arrays.stream(words)
        .collect(Collectors.toCollection(ArrayList::new));
```

**Listing 2.** `Collections.addAll` appends into an existing collection. `Collectors.toCollection(ArrayList::new)` is the stream path that **names** `ArrayList`. `Collectors.toList()` and `Stream.toList()` do **not** promise `ArrayList` (the latter is unmodifiable).

`List.of(words)` (Java 9+) also accepts the array and yields an **unmodifiable** list of the component type — useful when you want a `List`, not an `ArrayList`. Wrap with `new ArrayList<>(List.of(words))` if you need both the factory and a resizable copy. `List.of` rejects `null` elements (`NullPointerException`); `ArrayList` does not.

> [!warning] `Arrays.asList` is not a resizable `ArrayList`
> `view.add("fox")` throws `UnsupportedOperationException`. `view.set(0, "ACE")` **does** succeed and overwrites `words[0]`. If the interview asks for an `ArrayList`, stop after `asList` only when a fixed-size, array-backed `List` is enough.

> [!warning] A primitive array is one list element
> `T` in `asList(T...)` is a reference type. `Arrays.asList(new int[]{1, 2, 3})` is a `List<int[]>` of **size 1**. Box first (`Integer[]`), or stream with `Arrays.stream(int[])` and collect. Autoboxed varargs `Arrays.asList(1, 2, 3)` is three `Integer`s — still not `java.util.ArrayList`.

> [!tip] Interview answer
> **`new ArrayList<>(Arrays.asList(array))`.** `asList` is a fixed-size view of the same array: `set` writes through, `add`/`remove` throw. A real `ArrayList` copies the elements and can grow. Do not pass a primitive array to `asList` unless you want a one-element list of that array.
