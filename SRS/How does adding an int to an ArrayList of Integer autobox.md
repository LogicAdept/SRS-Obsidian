<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/Collections/List/ArrayList #SRS

# How does adding an `int` to an `ArrayList` of `Integer` autobox?

> [!abstract] Short answer
> `ArrayList<Integer>.add` takes `E`, which is `Integer`, not `int`. Passing a primitive is a **loose invocation** boxing conversion: the compiler treats `list.add(i)` as `list.add(Integer.valueOf(i))`. The list still stores wrapper objects. The reverse assignment `int n = list.get(k)` **unboxes** (`intValue()`), and throws `NullPointerException` if that slot is `null`.

## Why `add(int)` compiles on a list of `Integer`

You cannot declare `ArrayList<int>` — generic type arguments are reference types (see [[Why cannot Java collections store primitive types]]). `add(E e)` therefore expects an `Integer`. An `int` argument is not applicable under **strict** invocation (identity / widening primitive / widening reference). **Loose** invocation allows a boxing conversion, so the call is still legal.

Boxing an `int` produces an `Integer` whose `intValue()` equals that `int`. The usual implementation is `Integer.valueOf(i)`, which is what the Oracle autoboxing tutorial shows the compiler inserting. That factory always caches **-128..127** and may cache more — see [[What method does the compiler insert when autoboxing an int]] and [[When does autoboxing occur in Java]].

```d2
direction: down
src: "int i" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
box: "boxing\nInteger.valueOf(i)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
add: "ArrayList.add(Integer)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
store: "element is an Integer object" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}

src -> box
box -> add
add -> store
```

**Fig. 1.** The list API never sees a raw `int`; autoboxing happens on the argument.

```java
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 10; i++) {
    list.add(i); // list.add(Integer.valueOf(i))
}
int num = list.get(0); // unboxing → get(0).intValue()
```

**Listing 1.** Conceptual: the tutorial’s `add` pattern; `0..9` hit the `Integer` cache.

`ArrayList` also has `add(int index, E element)`. A **one-argument** `list.add(i)` is still `add(E)` with boxing, not an index insertion. The `int` index of the two-argument overload is a real primitive; only the element is boxed.

## Unboxing on the way out

`get` returns `Integer`. Using that result where an `int` is required (assignment, `+`, `%`, and so on) is unboxing conversion. A `null` element — `list.add(null)` is allowed — makes that unboxing throw `NullPointerException`, the same pitfall as [[How do you avoid NullPointerException when unboxing a Map value]].

Boxing itself may throw `OutOfMemoryError` if a new wrapper must be allocated.

> [!warning] Cache hits are not “no objects”
> Values in **-128..127** reuse interned `Integer` instances, so a tight `add` loop over small `int`s does not allocate one object per call. Values outside that range typically allocate. Either way the list holds **references**, and `==` between boxed elements is not a numeric compare.

> [!warning] `null` in the list is legal until you unbox
> `list.get(k)` returning `null` compiles; `int n = list.get(k)` does not survive at run time. Prefer `Integer` locally, or null-check, before converting to `int`.

> [!tip] Interview answer
> **`list.add(i)` on `ArrayList<Integer>` autoboxes: the compiler calls `Integer.valueOf(i)` and `add` stores that wrapper.** Collections cannot hold primitives. Getting the element back into an `int` unboxes and will NPE if the stored reference is `null`.
