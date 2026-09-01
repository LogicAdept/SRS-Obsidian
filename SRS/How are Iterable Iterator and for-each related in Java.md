<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Language/Loops #SRS

# How are Iterable, Iterator, and for-each related in Java?

> [!abstract] Short answer
> **`Iterable` produces an `Iterator`; enhanced `for` over an `Iterable` is sugar for that iterator.** `iterator()` is the bridge. The compiler rewrites `for (T x : iterable)` to `#i = iterable.iterator()` then `hasNext()` / `next()`. `Iterator` also works as an explicit cursor without for-each. Arrays are a second for-each target and use neither interface.

## Producer, cursor, syntax

```d2
direction: down
itb: "Iterable<T>\niterator()" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
itr: "Iterator<T>\nhasNext / next / remove" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
fe: "for (T x : expr)" {
  width: 240
  height: 50
  style.fill: "#eceff1"
}
arr: "array\nindex 0 .. length" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
itb -> itr
fe -> itb
fe -> arr
itr -> fe: "hidden #i"
```

**Fig. 1.** Three roles. `Iterable` is the type test for objects. `Iterator` is the walk. Enhanced `for` is the statement that hides the iterator — or, for arrays, hides an index.

`Iterable<T>` (1.5) exists so an object can be the target of enhanced `for`. Its abstract method returns `Iterator<T>`. Default `forEach` / `spliterator` (1.8) are not that rewrite; the `forEach` spec body *is* enhanced `for` [[What language feature enables the enhanced for each loop]], [[What must a class implement to support enhanced for each iteration]].

`Iterator<T>` (1.2) is the cursor: `hasNext`, `next`, optional `remove`. A collection class normally implements `Iterable` and returns a fresh iterator; it does not implement `Iterator` itself. You can still write `while (it.hasNext()) { it.next(); }` with no for-each at all [[How are Iterable and Iterator related in Java]], [[What is the Iterator interface and why do Java collections use it]].

Enhanced `for` is the language statement. If `expr` is a subtype of `Iterable`, the meaning is a basic `for` over a generated `#i`. If `expr` is an array, the meaning is `0 .. length` and there is no `Iterator`. Anything else is a compile-time error [[How would you explain the enhanced for each loop in Java]].

`Collection` extends `Iterable`, so every JDK collection is already a for-each target. Your own type needs `Iterable`, not `Collection` [[What must a class implement to support enhanced for each iteration]].

```java
class TrioDemo {
    static void allThree(Iterable<String> words, String[] letters) {
        java.util.Iterator<String> it = words.iterator();
        while (it.hasNext()) {
            System.out.println(it.next());
        }

        for (String w : words) {
            System.out.println(w);
        }

        for (String ch : letters) {
            System.out.println(ch);
        }
    }
}
```

**Listing 1.** Same `Iterable` walked twice: once with an explicit `Iterator`, once with for-each (a hidden iterator). `letters` is an array; that loop never calls `iterator()`.

Because `#i` is synthetic, a for-each body cannot call `Iterator.remove()`. Structural `coll.remove` during that walk is the fail-fast / unspecified path [[Can you modify a collection while iterating with a for-each loop]].

> [!warning] For-each is not “always Iterator”
> `int[]` and `String[]` work in enhanced `for` and do **not** implement `Iterable`. Answering this cue with “for-each always uses `Iterator`” is wrong for arrays.

> [!warning] Implementing `Iterator` does not enable for-each
> The type test is `Iterable` (or array). A class that implements only `Iterator` is a cursor, not a for-each target — unless it also implements `Iterable` and `iterator()` returns an `Iterator` (often a new one per call). Duck-typed `iterator()` without `implements Iterable` does not compile.

> [!tip] Interview answer
> **`Iterable` supplies `iterator()`; `Iterator` is the cursor; for-each over an `Iterable` is hidden `hasNext` / `next`.** Implement `Iterable` to use for-each on your type. Arrays are the other for-each shape and skip both interfaces. Use an explicit `Iterator` when you need `remove()`.
