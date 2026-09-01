<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/Language/Primitives #Java/Performance #SRS

# Is autoboxing always a performance problem in Java?

> [!abstract] Short answer
> **No.** Autoboxing is the intended way to bridge primitives and collections. Oracle’s language guide calls that “impedance mismatch” use **plenty fast enough for occasional** `get`/`set`/list work, and calls boxing in a **performance-critical inner loop** folly. Allocation is also not guaranteed: `valueOf` **reuses** **-128..127**, and HotSpot escape analysis may **scalar-replace** a wrapper that never leaves the method.

## When the spec authors say it is fine

Boxing exists so you can put an `int` into a `List<Integer>` without writing `Integer.valueOf` at every call (see [[How does adding an int to an ArrayList of Integer autobox]]). The JDK 5 autoboxing guide’s `int[]`→`List<Integer>` adapter boxes on every `get`/`set` and still describes that as acceptable for **occasional** use. The same page says **not** to use autoboxing for scientific computing or other performance-sensitive numerical code: an `Integer` is not a substitute for an `int`.

So “always a problem” is the wrong takeaway. The feature is for the collection/API boundary; the tax is repeated boxing in a hot numeric loop.

```d2
direction: down
ok: "Occasional box\nlist.add(i), return Integer" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
hot: "Inner loop / accumulator\nLong total += k" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
mit: "Cache -128..127\nescape analysis may delete alloc" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}

ok -> ok: "designed use"
hot -> hot: "folly per language guide"
mit -> hot: "may hide cost, do not rely"
```

**Fig. 1.** Occasional collection boxing is the point of the feature; tight-loop boxing is the performance case.

```java
List<Integer> list = new ArrayList<>();
list.add(3);                 // cache hit; intended use

Long total = 0L;
for (long k = 0; k < 1_000_000; k++) {
    total += k;              // unbox, add, box; k quickly leaves -128..127
}
```

**Listing 1.** Conceptual: one `add` versus a boxed accumulator (see [[What happens when you use Integer as a loop accumulator in Java]]).

## Why it is not “always” a heap storm

`Integer.valueOf` / `Long.valueOf` **always cache** **-128..127**. Boxing `list.add(i)` for `i` in `0..9` reuses interned instances rather than allocating one object per call. Values outside that range typically allocate a new wrapper (object header + payload — [[How much memory does an Integer object use compared with int]]).

HotSpot escape analysis can classify a wrapper as `NoEscape` and **eliminate the allocation** (scalar replacement). That is why a microbenchmark of a local `Integer` sometimes shows no heap traffic — and why you still should not write [[Why prefer primitives over wrappers in hot loops in Java]] as wrappers and hope the JIT saves you.

> [!warning] A boxed accumulator is the actual trap
> `Long total = 0L; total += k;` looks like a primitive add. It unboxes, adds, and boxes on **every** iteration. After 127 the `Long` cache no longer absorbs it, so you allocate and discard wrappers at loop rate. Use `long total`. The same pattern with `Integer` in a `for` condition is equally wrong.

> [!warning] “Cached” is not “free”
> Cache hits avoid **new** objects; they do not make `Integer` an `int`. You still pay extra pointer chasing, cannot use `==` as numeric equality, and unboxing `null` throws. Compact object headers and compressed oops change instance size; they do not make inner-loop boxing cheap.

> [!tip] Interview answer
> **No — autoboxing is for the primitive/collection boundary, not a universal slowdown.** Occasional `list.add(i)` is the designed use; boxing inside a tight numeric loop or using `Long`/`Integer` as an accumulator is the problem. Small values may hit the **-128..127** cache, and escape analysis may even delete a local wrapper, so “always allocates” is false — still write primitives in hot code.
