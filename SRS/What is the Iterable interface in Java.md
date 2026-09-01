<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Language #SRS

# What is the `Iterable` interface in Java?

> [!abstract] Short answer
> **`java.lang.Iterable<T>` is the for-each target type (Java 5).** Implementing it lets an object appear after `:` in `for (T x : obj)`. The one abstract method is `Iterator<T> iterator()`, which must return a **new** cursor each call. Java 8 added default `forEach` and `spliterator`. `Collection` extends `Iterable`. `Iterator` does not.

## Source of iterators, not the cursor

`Iterable` exists so a type can be the expression of the enhanced `for` statement. The compiler calls `iterator()`, then `hasNext()` / `next()` on a hidden iterator [[How are Iterable Iterator and for-each related in Java]], [[Can you use enhanced for with your own class in Java]], [[What must a class implement to support enhanced for each iteration]].

You do not need to implement `Collection`. You must not return `null` from `iterator()` (the loop calls it immediately). Nested for-each over the same object needs two independent iterators — returning `this` if the type also implements `Iterator` shares one cursor and breaks inner loops [[How are Iterable and Iterator related in Java]].

**Java 8 defaults:** `forEach(Consumer)` is specified as enhanced `for` over `this`. `spliterator()` default builds an early-binding spliterator from `iterator()` (poor split; collections override). `Collection.stream()` uses the spliterator.

**Related types:** `Iterator` is the walker (`hasNext`/`next`/`remove`) since 1.2 [[What interface lets you traverse elements of a Java collection]], [[In which Java version was Iterator introduced]]. `Map` is not `Iterable`; walk `keySet()` / `values()` / `entrySet()`. Arrays are for-each targets **without** `Iterable`.

```d2
direction: down
itb: "Iterable<T>\nJava 5" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
m: "iterator()" {
  width: 160
  height: 45
}
cur: "Iterator<T>" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
fe: "for (T x : iterable)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

fe -> itb -> m -> cur
```

**Fig. 1.** `Iterable` produces iterators. For-each never takes an `Iterator` in the `:` slot.

```java
final class Names implements java.lang.Iterable<String> {
    private final String[] items;

    Names(String... items) {
        this.items = items;
    }

    @Override
    public java.util.Iterator<String> iterator() {
        return java.util.Arrays.asList(items).iterator();
    }
}
```

**Listing 1.** A non-`Collection` `Iterable`. `for (String s : new Names("a", "b"))` is legal. `iterator()` must not return `null`.

> [!warning] `Iterator` is not `Iterable`
> `for (E e : someIterator)` does not compile. `Enumeration.asIterator()` still returns an `Iterator`. Implement `Iterable` or use a `while` loop.

> [!warning] One abstract method, not “only one method”
> Since Java 8 you also inherit `forEach` and `spliterator`. You still write `iterator()`. Overriding `forEach` does not change enhanced `for` unless you also change `iterator()`.

> [!tip] Interview answer
> **`Iterable` is the Java 5 interface that makes a type a for-each target: implement `iterator()` and return an `Iterator`.** `Collection` is Iterable. Iterator is the cursor, a different type from 1.2. Arrays work in for-each without Iterable.
