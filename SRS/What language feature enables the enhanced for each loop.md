<!--
reps: 0
priority: 0
-->
#Java/Language/Loops #Java/Collections/Iteration #SRS

# What language feature enables the enhanced for each loop?

> [!abstract] Short answer
> **`java.lang.Iterable`**. Implementing that interface makes an object a legal target of `for (T x : obj)`. The compiler calls `obj.iterator()` and then `hasNext()` / `next()`. **Arrays** are the other legal target; they do **not** implement `Iterable` — the compiler emits an index loop instead.

## The type test

```d2
direction: down
expr: "expr in for (T x : expr)" {
  width: 280
  height: 50
  style.fill: "#eceff1"
}
it: "subtype of Iterable\niterator() → hasNext / next" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
arr: "array type\n0 .. length, x = a[i]" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
err: "anything else\ncompile-time error" {
  width: 300
  height: 60
  style.fill: "#ffebee"
}
expr -> it
expr -> arr
expr -> err
```

**Fig. 1.** Two enabling shapes. `Iterable` is the object-side language feature; arrays are a built-in special case.

`Iterable<T>` has been in `java.lang` since **1.5**, the same release as enhanced `for`. Its contract is one abstract method: `Iterator<T> iterator()`. Default `forEach` / `spliterator` arrived later and are **not** what the loop uses.

The rewrite of the loop itself: [[How would you explain the enhanced for each loop in Java]]. Making your type a target: [[What must a class implement to support enhanced for each iteration]], [[Can you use enhanced for with your own class in Java]].

```java
class EnableForEach {
    public static void main(String[] args) {
        Iterable<String> words = java.util.List.of("for", "each");
        for (String w : words) {
            System.out.println(w);
        }

        char[] cs = {'J', 'L', 'S'};
        for (char c : cs) {
            System.out.println(c);
        }
        // for (char c : words) { }  // compile-time error: Iterable<String>, not char[]
    }
}
```

**Listing 1.** `words` is typed `Iterable<String>`, so the loop calls `iterator()`. `char[]` is an array type. `words` is not an array of `char`.

A method parameter typed `Iterable<T>` is enough to for-each. You do not need a concrete list type in the header. A type that is neither an array nor `Iterable` does not compile as `expr`.

> [!warning] Arrays are not `Iterable`
> `int[]` and `String[]` work as `expr` without implementing any interface. The compiler does not call `iterator()` on an array. Answering this cue with “arrays implement `Iterable`” is wrong.

> [!warning] `Iterable.forEach` does not enable the loop
> `forEach(Consumer)` is a **default method** (1.8) whose spec implementation is `for (T t : this) action.accept(t)`. The statement enables `forEach`, not the other way around. You still cannot `continue` / `break` a surrounding loop from inside that lambda the way you can from enhanced `for`.

> [!tip] Interview answer
> **`Iterable` — if a class implements it, enhanced `for` can iterate it by calling `iterator()`.** Arrays are the other target and do not implement `Iterable`. The type test is `Iterable` or array; a concrete list type is not required.
