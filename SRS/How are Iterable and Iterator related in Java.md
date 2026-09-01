<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Language #SRS

# How are `Iterable` and `Iterator` related in Java?

> [!abstract] Short answer
> **`Iterable` is the source; `Iterator` is the cursor.** `Iterable.iterator()` returns a **new** `Iterator` over that source. Enhanced `for` requires an `Iterable` (or an array) and calls `iterator()` for you. `Iterator` does **not** extend `Iterable`. `Iterable` does **not** extend `Iterator`.

## Producer and cursor

`Iterable<T>` (Java 5) is the type you walk with enhanced `for`. Its abstract method is `Iterator<T> iterator()`. Each call should produce a **fresh** cursor so nested loops do not share position [[What is the Iterable interface in Java]], [[Can you use enhanced for with your own class in Java]].

`Iterator<T>` (Java 1.2) is the cursor: `hasNext` / `next`, optional `remove` [[What is the Iterator interface and why do Java collections use it]], [[In which Java version was Iterator introduced]]. It is **not** a for-each target. `for (E e : someIterator)` does not compile unless that object is also `Iterable`.

Java 8 added **default** methods on `Iterable`: `forEach` (implemented as enhanced `for` over `this`) and `spliterator` (default: early-binding spliterator from `iterator()`). So `Iterable` is no longer a single-method interface. `iterator()` is still the one abstract method you must write [[How are Iterable Iterator and for-each related in Java]].

`Collection` extends `Iterable`; `collection.iterator()` is the same factory. `Map` is not `Iterable`; `keySet()` / `values()` / `entrySet()` are.

The enhanced-`for` translation for an `Iterable` is: obtain `#i = expr.iterator()`, then `while (#i.hasNext()) { T x = #i.next(); … }`. That is the whole relationship the language uses.

```d2
direction: down
src: "Iterable<T>\niterator()" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
cur: "Iterator<T>\nhasNext / next / remove" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
loop: "for (T x : iterable)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}

src -> cur
loop -> src
```

**Fig. 1.** The loop never takes an `Iterator` in the `:` slot. It asks the `Iterable` for one.

```java
class IterableProducesIterator {
    static void walk(java.lang.Iterable<String> source) {
        java.util.Iterator<String> first = source.iterator();
        java.util.Iterator<String> second = source.iterator();
        while (first.hasNext()) {
            first.next();
        }
        for (String s : source) {
            System.out.print(s);
        }
    }
}
```

**Listing 1.** Two `iterator()` calls are two independent cursors. The enhanced `for` is a third call. Exhausting `first` does not exhaust `second` or the for-each.

> [!warning] `Iterator` is not `Iterable`
> Returning an `Iterator` from a method does not make that value for-each-able. Implement `Iterable` (or pass `iterator()` to a `while`). `Enumeration.asIterator()` still returns an `Iterator`.

> [!warning] “Only one method” is Java 5 news
> Today `Iterable` also has default `forEach` and `spliterator`. You still implement **one** abstract method: `iterator()`. Do not implement `Iterator` on the collection type itself unless you also implement `Iterable` and return `this` from `iterator()` — that shared cursor is a trap for nested loops.

> [!tip] Interview answer
> **`Iterable.iterator()` creates an `Iterator`.** Iterable is what enhanced `for` accepts; Iterator is the walk (`hasNext`/`next`). They are different interfaces. Collection is Iterable; a raw Iterator is not.
