<!--
reps: 0
priority: 0
-->
#Java/Collections/Sorting/Comparable #Java/Collections/Sorting/Comparator #SRS

# What is the difference between `java.lang.Comparable` and `java.util.Comparator`?

> [!abstract] Short answer
> **`Comparable` (`java.lang`) is the type's own `compareTo` — one natural order, on the instance.** **`Comparator` (`java.util`) is an external `compare(a, b)` — many orders, a separate object (often a lambda).** Extra sorts (name vs age vs email) are extra comparators, not extra `compareTo` methods. There is no `Comparator.compareTo`.

## Instance `compareTo` versus two-argument `compare`

| | `java.lang.Comparable<T>` | `java.util.Comparator<T>` |
| --- | --- | --- |
| Method | `int compareTo(T o)` — **this** vs `o` | `int compare(T o1, T o2)` — two arguments |
| Who implements it | The element type itself | A separate class, lambda, or method reference |
| How many | One natural ordering per class | As many as you need |
| Sort / map API | `Collections.sort(list)`, `Arrays.sort`, `list.sort(null)`, `new TreeMap<>()` | `sort(list, c)`, `list.sort(c)`, `new TreeMap<>(c)` |
| Nulls | `compareTo(null)` should throw `NullPointerException` | May permit nulls (`nullsFirst` / `nullsLast`) |
| Lambda | Comparison lives on the instance | `@FunctionalInterface` — assignment target for a lambda |

Both return negative / zero / positive for less / equal / greater. Both require the same `signum` and transitivity rules. Both since 1.2. `Comparator` grew static/default factories in 8 (`comparing`, `thenComparing`, `naturalOrder`, `reversed`).

`Comparable` is how a class **is** ordered. Objects that implement it sort with `Collections.sort` / `Arrays.sort` and `list.sort(null)`, and can be sorted-map keys or sorted-set elements **without** a comparator.

`Comparator` is how you **impose** an order: precise control over `sort`, control of a `TreeMap` / `TreeSet`, or an order for a type that has no natural ordering — including when it *has* `compareTo` but this call site needs a different one.

```d2
direction: right
cbl: "java.lang.Comparable\nthis.compareTo(o)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
cpr: "java.util.Comparator\ncompare(o1, o2)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
nat: "one natural order\non the type" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
ext: "external order\nmany per type" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
cbl -> nat
cpr -> ext
```

**Fig. 1.** Package and method name mark the split: natural order on the instance vs an injected two-arg function. Passing a comparator into `TreeMap`: [[How do you customize TreeMap key order]].

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Item implements Comparable<Item> {
    final String sku;
    final int qty;

    Item(String sku, int qty) {
        this.sku = sku;
        this.qty = qty;
    }

    @Override
    public int compareTo(Item o) {
        return this.sku.compareTo(o.sku); // the one natural order
    }
}

class Demo {
    static void naturalVersusExternal() {
        List<Item> items = new ArrayList<Item>();
        items.add(new Item("b", 10));
        items.add(new Item("a", 30));
        items.add(new Item("a", 20));

        items.sort(null); // SKU — [a/30, a/20, b/10] (stable; both "a" stay)
        items.sort(Comparator.comparingInt(i -> i.qty)); // by qty
        items.sort(Comparator.comparing((Item i) -> i.sku)
                .thenComparingInt(i -> i.qty)); // thenComparing only if compare == 0
    }

    static void stringNaturalVersusIgnoreCase() {
        List<String> names = new ArrayList<String>();
        names.add("Zebra");
        names.add("apple");
        names.sort(null);                          // String.compareTo
        names.sort(String.CASE_INSENSITIVE_ORDER); // Comparator, not compareTo
    }
}
```

**Listing 1.** One `compareTo` (SKU). Qty and SKU-then-qty are comparators, not more `compareTo` methods. `list.sort(null)` is natural order. A lambda is legal for `Comparator` [[How do you sort a list of strings with a lambda in Java]]; it is not how you implement `Comparable`.

> [!warning] There is no `Comparator.compareTo`
> The usual mix-up is `compare` vs `compareTo`. `Comparable.compareTo` is the instance method. `Comparator.compare` is the two-arg method. Same sign convention, different names and receivers. Writing `Comparator.compareTo` does not compile. `ClassCastException` if the other object's type cannot be compared.

> [!warning] Same sign contract, different uniqueness
> `compare == 0` / `compareTo == 0` should match `equals` (consistent with equals). A `TreeMap` / `TreeSet` with no extra comparator treats that as **the same key** [[Why must TreeMap ordering be consistent with equals]]. `List.sort` is stable and keeps both rows. `BigDecimal` is the core-library exception (`4.0` vs `4.00` compare equal, `equals` is false) — recommended note: "this class has a natural ordering that is inconsistent with equals." `naturalOrder()` / `reverseOrder()` still NPE on null; wrap `nullsFirst` / `nullsLast`.

> [!tip] Interview answer
> **`Comparable` is `java.lang` — `compareTo` on the object, one natural order, used when `sort` or `TreeMap` gets no comparator. `Comparator` is `java.util` — `compare(a, b)` on a separate object, as many orders as you want (name, age, email), including lambdas since 8. Do not write three `compareTo` methods for three sorts; the method on a comparator is `compare`, not `compareTo`. `compare == 0` is uniqueness in a tree, not on a `List`.**
