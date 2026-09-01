<!--
reps: 0
priority: 0
-->
#Java/Language/Loops #Java/Collections/Iteration #SRS

# How would you explain the enhanced for each loop in Java?

> [!abstract] Short answer
> `for (T x : expr)` walks **elements**, not indexes. `expr` must be an **array** or a subtype of `Iterable`. The language rewrites it to a basic `for`: arrays use `0 .. length`; `Iterable` uses `iterator()` / `hasNext()` / `next()`. Each trip assigns the next element to a **fresh local** `x`. That is a second form of `for`, not a fifth loop statement.

## Syntax and rewrite

```d2
direction: down
header: "for (T x : expr)" {
  width: 260
  height: 50
  style.fill: "#eceff1"
}
split: "type of expr?" {
  width: 200
  height: 50
}
arr: "array S[]\n#a = expr once\nfor i in 0..#a.length\nx = #a[i]" {
  width: 280
  height: 110
  style.fill: "#e3f2fd"
}
it: "Iterable\n#i = expr.iterator()\nwhile #i.hasNext()\nx = #i.next()" {
  width: 280
  height: 110
  style.fill: "#e8f5e9"
}
header -> split
split -> arr
split -> it
```

**Fig. 1.** One header, two translations. `expr` is evaluated **once**. `#a` / `#i` are generated names you cannot see or `remove()` through.

Anything else is a compile-time error: not an array, not `Iterable`, a header with an initializer (`for (int x = 0 : a)`), or more than one declared variable. `var x` takes the array component type, or `X` from `Iterable<X>`, or `Object` from a raw `Iterable`.

The other `for` / `while` / `do` shapes: [[How would you explain kinds of loops in Java]], [[How do Java for, while, and do-while loops differ]]. Why `Iterable` is the type that unlocks this: [[What language feature enables the enhanced for each loop]], [[What must a class implement to support enhanced for each iteration]].

```java
class EnhancedForDemo {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        for (int item : numbers) {
            System.out.println("Count is: " + item);
        }
    }
}
```

**Listing 1.** Array for-each. Same output as `for (int i = 0; i < numbers.length; i++)` printing `numbers[i]`, without an index in scope. The element type may unbox: `for (int n : histogram.values())` is legal when `values()` yields `Integer`.

```java
class BindLocal {
    static void demo() {
        int[] a = {1, 2, 3};
        for (int x : a) {
            x = 0;
        }
        // a is still {1, 2, 3}

        int[][] rows = {{1, 2}, {3, 4}};
        for (int[] row : rows) {
            row[0] = 0;
        }
        // rows[0][0] and rows[1][0] are 0: row is a reference
    }
}
```

**Listing 2.** Reassignment of the loop variable never writes the source. Mutation **through** a reference element does. `null` as `expr` throws `NullPointerException` on `iterator()` or on `#a.length`.

Use this form when you need each element and not the index. Keep a basic `for` for reverse walks, lockstep over two arrays, or an iterator you can `remove()` from. Your own type works when it is `Iterable`: [[What must a class implement to support enhanced for each iteration]]. Changing a collection while this loop runs is the iterator contract: [[Can you modify a collection while iterating with a for-each loop]].

> [!warning] The loop variable is not an alias for the slot
> `for (int x : a) x = 0` copies the `int`. `for (String s : list) s = "z"` rebinds a local; the list is unchanged. Only if the element is a mutable object, and you call a mutator on it, does the collection’s object graph change.

> [!warning] No index, no `remove()`, one snapshot of `expr`
> There is no `i` unless you maintain one yourself. The iterator is synthetic, so you cannot call `Iterator.remove()`. `expr` is captured at entry; swapping the array variable afterward does not redirect the loop.

> [!tip] Interview answer
> **Enhanced `for` is `for (T x : arrayOrIterable)` — a `for` that binds each element to a local.** Arrays become an index loop; `Iterable` becomes `iterator()` / `hasNext()` / `next()`. Assigning to `x` does not update the source; use a basic `for` when you need the index or to remove.
