<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Sorting #Java/Lambdas #Java/Versions/8 #SRS

# How do you list string with using lambda

> [!abstract] Short answer
> **Pass a `Comparator` lambda to `Collections.sort` or `List.sort`.** `(a, b) -> a.compareTo(b)` is `Comparator.compare` and sorts `List<String>` in `String`’s lexicographic natural order. The list is **mutated in place**. Same order: `String::compareTo`, `Comparator.naturalOrder()`, or `Collections.sort(list)` with no comparator.

## Lambda as `Comparator`, sort as a mutating API

`Comparator` is a `@FunctionalInterface`: one abstract method `compare(T, T)` → `int`. A Java 8 lambda (or method reference) is a legal argument to `Collections.sort(list, c)` and to `List.sort(c)` (`@since 1.8`). In Java 8, `Collections.sort(list, c)` **defers to** `List.sort` ([[How do you sort a list of strings with a lambda in Java]], [[How would you explain lambda expressions in Java]], [[What is the difference between java.lang.Comparable and java.util.Comparator]]).

`String.compareTo` compares lexicographically by Unicode code units. It returns `0` exactly when `equals` is true. `(a, b) -> a.compareTo(b)` is that natural order. `String::compareTo` is the same lambda. `compareToIgnoreCase` / `String::compareToIgnoreCase` is a different order ([[What is method reference]]).

The sort is **stable** (equal elements keep relative order). The list must be **modifiable** but need not be resizable. Unmodifiable lists throw `UnsupportedOperationException` when the iterator cannot `set`. `null` comparator means natural order (`Comparable`). `null` elements make `compareTo` throw `NullPointerException`.

```d2
direction: down
lam: "(a, b) -> a.compareTo(b)\nComparator<String>" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
sort: "Collections.sort / List.sort\nin-place, stable" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
out: "same List, lexicographic order" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}

lam -> sort -> out
```

**Fig. 1.** The lambda is the comparator. The sort rewrites the list; it does not return a new list ([[What is the Stream sorted method for]]).

```java
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

class Demo {
    static List<String> sortNatural(List<String> list) {
        Collections.sort(list, (a, b) -> a.compareTo(b));
        return list;
    }

    static void equivalents(List<String> list) {
        list.sort(String::compareTo);
        list.sort(Comparator.naturalOrder());
        list.sort(Comparator.reverseOrder());
    }
}
```

**Listing 1.** Dump shape is legal: `sort` returns the same instance after an in-place sort. `list.sort(...)` is the Java 8 instance form. Reverse uses `reverseOrder()` / `reversed()`, not a second “list” API.

`stream().sorted()` leaves the source list alone and needs a terminal. That is a different question from `Collections.sort`.

> [!warning] In-place: the caller’s list changes
> `Collections.sort` / `List.sort` rewrite the list you passed in. `List.of("b", "a").sort(...)` throws `UnsupportedOperationException`. Copy first if you need both the original and a sorted view: `new ArrayList<>(list)` then sort the copy.

> [!warning] `compareTo` is not null-safe and not case-folding
> A `null` string → `NullPointerException`. `"A"` and `"a"` are different Unicode values. For nulls use `Comparator.nullsFirst(Comparator.naturalOrder())` (or `nullsLast`). For case-insensitive order use `String::compareToIgnoreCase`, not `toLowerCase` inside a lambda that allocates on every compare.

> [!tip] Interview answer
> **`Collections.sort(list, (a, b) -> a.compareTo(b))` or `list.sort(String::compareTo)`.** The lambda is a `Comparator`; the sort is in-place and stable. Natural order is already `Collections.sort(list)` with no comparator. Stream `sorted()` does not mutate the list.
