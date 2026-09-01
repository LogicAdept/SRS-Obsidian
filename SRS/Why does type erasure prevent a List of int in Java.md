<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/Generics #SRS

# Why does type erasure prevent a `List` of `int` in Java?

> [!abstract] Short answer
> Generics **erase** to a single raw class whose slots are **object references**. `List<Integer>` and `List<String>` are both `List` at run time; the compiler throws away `E` (unbounded → `Object`) and inserts casts. An `int` is not a reference, so it cannot live in those slots — and the language never lets you write `List<int>` because type arguments must be reference types. Use `List<Integer>` (autobox) or `int[]` (reifiable primitive array).

## One `List` class, reference-sized cells

Erasure maps a parameterized type `G<T1,…>` to `|G|` — the raw class. A type variable without a tighter bound erases to `Object`. The bytecode contains ordinary classes only; there is **no** generated `ListOfInt`. Compatibility with pre-generic `List` of `Object` is why that mapping exists.

So even if `List<int>` parsed, the runtime layout would still be “list of references.” A 32-bit `int` is not an `Object`. Wrappers exist so the payload *is* a reference ([[Why cannot Java collections store primitive types]], [[Why are wrapper classes needed in Java]]).

```d2
direction: down
src: "List<Integer> / List<String>" {
  width: 280
  height: 50
}
erase: "erasure → raw List\nslots are references" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
bad: "List<int>\nnot a type argument" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
src -> erase
```

**Fig. 1.** Parameterizations collapse to one class; primitives have nowhere to sit.

```java
List<Integer> ints = new ArrayList<>();
ints.add(1);                     // valueOf — the cell holds an Integer

// List<int> no = new ArrayList<>();  // compile error: primitive type argument

int[] raw = { 1, 2, 3 };         // primitive array — reifiable, not generic
```

**Listing 1.** Conceptual: erasure + boxing vs a real `int[]` ([[How does adding an int to an ArrayList of Integer autobox]], [[Why does autoboxing exist in Java]]).

This is not special to `ArrayList`. Any generic type (`Map<K,V>`, `Optional<T>`, your `Pair<K,V>`) has the same rule. Primitive arrays work because `int[]` is a **reifiable** array type, not a parameterization.

> [!warning] Erasure is the why; `List<int>` is already a compile error
> The compiler rejects `List<int>` because type arguments must be references — you never get as far as a botched runtime layout. Saying “erasure deletes `int`” is sloppy: `int` was never a legal `E`. Erasure explains **why** generics were designed that way (one `List`, `Object` cells).

> [!tip] Interview answer
> **`List<E>` erases to a list of references, so there is no cell for a bare `int`.** Type arguments have to be objects, which is why you write `List<Integer>` and autobox. `int[]` can store primitives because it is not generic. Same story for every generic type, not just `ArrayList`.
