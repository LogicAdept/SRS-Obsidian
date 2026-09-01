<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Sorting/Comparator #Java/Lambdas #Java/String #Java/Versions/8 #SRS

# How do you sort a list of strings with a lambda in Java?

> [!abstract] Short answer
> Call `list.sort((a, b) -> a.compareTo(b))`. `Comparator` is a **functional interface**, so a two-argument lambda (or `String::compareTo`) is the comparator. That is `String` **natural order**: Unicode code units, not dictionary case. For a key, prefer `Comparator.comparingInt(String::length).thenComparing(...)`. Java 8: `List.sort` and the `comparing*` factories.

## A lambda is a `Comparator`

`Comparator.compare(T, T)` returns negative, zero, or positive as the first argument is less than, equal to, or greater than the second. Because the type is `@FunctionalInterface`, a lambda is a legal `Comparator<String>`:

```text
(a, b) -> a.compareTo(b)
```

`list.sort(comparator)` (Java 8) sorts **this** list in place. The sort is **stable**: equal elements keep their relative order. All elements must be mutually comparable under that comparator (`ClassCastException` otherwise). A `null` comparator means natural order (`Comparable.compareTo`) — for `String` that is the same Unicode `compareTo`. `Collections.sort(list)` with no comparator is that natural order. `Collections.sort(list, comparator)` defers to `List.sort`. `stream().sorted()` leaves the source list alone and needs a terminal; that is not `List.sort` ([[What is the Stream sorted method for]]).

`String.compareTo` compares lexicographically by Unicode value of each character. `'Z'` (90) is less than `'a'` (97), so `"Zebra"` precedes `"apple"`. Equal strings: `compareTo` is `0` exactly when `equals` is true. Shorter is less when one is a prefix of the other.

The list must be **modifiable** (it uses `set`) but **need not be resizable**. Default implementation: copy to an array, TimSort the array, write back with `set`.

```d2
direction: down
lam: "(a, b) -> a.compareTo(b)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
fi: "Comparator.compare" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
sort: "list.sort(c)  (Java 8)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
out: "same list, new order" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
lam -> fi
fi -> sort
sort -> out
```

**Fig. 1.** The lambda is the `compare` method. `list.sort` rewrites positions. Natural-order `String` vs an external `Comparator`: [[What is the difference between java.lang.Comparable and java.util.Comparator]]. Lambdas and method references: [[How would you explain lambda expressions in Java]], [[What is method reference]].

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

class Demo {
    static void lambdaNaturalOrder() {
        List<String> names = Arrays.asList("Zebra", "apple", "Banana");
        names.sort((a, b) -> a.compareTo(b));
        // [Banana, Zebra, apple] — 'B' < 'Z' < 'a'
        names.sort(String::compareTo);           // same ordering
        names.sort(Comparator.naturalOrder());   // same; NPE on null
        names.sort(Comparator.reverseOrder());  // descending Unicode order
    }

    static void byLengthThenIgnoreCase() {
        List<String> names = new ArrayList<String>();
        names.add("Zebra");
        names.add("apple");
        names.add("Banana");
        names.sort(Comparator.comparingInt(String::length)
                .thenComparing(String.CASE_INSENSITIVE_ORDER));
        // [apple, Zebra, Banana] — length 5, then 5, then 6
    }

    static void nullsLastNatural() {
        List<String> names = new ArrayList<String>();
        names.add("b");
        names.add(null);
        names.add("a");
        names.sort(Comparator.nullsLast(Comparator.naturalOrder()));
        // [a, b, null]
    }
}
```

**Listing 1.** Direct lambda / method reference / `naturalOrder` are Unicode `compareTo`. The `comparingInt` + `thenComparing` form is the documented composition for length then case-insensitive order (`CASE_INSENSITIVE_ORDER` is `compareToIgnoreCase`, not a locale `Collator`). `comparing*` / `thenComparing` / `nullsLast` are Java 8. `Arrays.asList` is fixed-size but sortable (`set` works). A descending **view** of an already-ordered list is a different API: [[How do you reverse a List in Java]].

> [!warning] Unmodifiable lists throw; `null` strings NPE
> `List.of("b", "a")` cannot replace elements: `sort` throws `UnsupportedOperationException`. Copy into an `ArrayList` first. A lambda that calls `a.compareTo(b)` (and `naturalOrder()` / `reverseOrder()`) throws `NullPointerException` on a `null` element — `Comparator` may permit nulls, but `String` natural order does not. Wrap with `nullsFirst` / `nullsLast`. `CASE_INSENSITIVE_ORDER` / `String::compareToIgnoreCase` still does not take locale into account. Do not `toLowerCase` inside the comparator; that allocates on every compare.

> [!warning] `compare == 0` is not uniqueness on a `List`
> A length-only comparator treats `"One"` and `"Two"` as equal for ordering. `List.sort` keeps both (stable). The same comparator on a `TreeMap` would collapse them [[How do you customize TreeMap key order]]. Tie-break with `thenComparing(Comparator.naturalOrder())` when you want lexicographic order among equal keys. A comparator that always returns `1` violates the `compare` contract (`signum` / transitivity); `sort` may throw `IllegalArgumentException`.

> [!tip] Interview answer
> **`list.sort((a, b) -> a.compareTo(b))` — `Comparator` is a functional interface, so that lambda is the sort order. For strings that is Unicode natural order, so uppercase precedes lowercase; use `comparingInt(String::length).thenComparing(String.CASE_INSENSITIVE_ORDER)` for a key. The list must support `set`; `List.of` throws, `Arrays.asList` does not.**
