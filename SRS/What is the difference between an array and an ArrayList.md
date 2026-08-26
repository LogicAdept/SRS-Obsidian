<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Arrays #SRS

# Array vs `ArrayList`

> [!abstract] Short answer
> An **array** is a fixed-length language object: after creation its `length` never changes, and it may hold primitives or references. An **`ArrayList`** is a resizable `List` over a private object array: logical size is `size()`, capacity can grow on `add`, and elements are references only (primitives are boxed).

## Fixed length vs growing capacity

```d2
direction: right
array: "array\nlength fixed at creation\ncomponents[0..n-1]" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
list: "ArrayList\nsize ≤ capacity\nbacking Object[] grows" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
array -> list: "same idea\n(contiguous slots)" {
  style.stroke-dash: 3
}
```

**Fig. 1.** Both store elements in contiguous slots; only `ArrayList` reallocates a larger backing array when capacity is exhausted.

JLS rule: once an array object exists, its length never changes — to “grow,” you assign a different array to the variable. `ArrayList` keeps a separate logical size and grows capacity automatically; growth policy is unspecified beyond **amortized constant-time** append. Prefer `new ArrayList<>(expectedSize)` or `ensureCapacity` when you know the eventual size.

```java
int[] fixed = new int[3];          // length == 3 forever
fixed[0] = 1;

List<Integer> growing = new ArrayList<>(3); // capacity hint, size == 0
growing.add(1);
growing.add(2);
System.out.println(fixed.length);  // 3
System.out.println(growing.size()); // 2
```

**Listing 1.** Array `length` is the slot count; `ArrayList.size()` is how many elements were added.

## Primitives, boxing, and access cost

Arrays may use a primitive element type (`int[]`, `long[]`, …). `ArrayList` implements `List<E>` and stores **references**, so an `int` becomes an `Integer` via autoboxing on `add` / unboxing on `get` — see [[How does adding an int to an ArrayList of Integer autobox]].

Documented `ArrayList` costs (Java SE 21): `get` / `set` are constant time; end `add` is **amortized** constant time (a resize copies the backing array). Indexed array access is also constant time. Saying “array is always faster” is too blunt: for reference elements with no resize, both are random-access; for dense primitives, a primitive array avoids wrapper objects and boxing.

```java
int[] ints = {1, 2, 3};
List<Integer> boxed = new ArrayList<>();
for (int v : ints) {
    boxed.add(v); // autobox to Integer
}
```

**Listing 2.** Same numbers: array keeps primitives; `ArrayList` stores `Integer` objects.

## Type checks: `ArrayStoreException` vs generics

Reference arrays are **reifiable** and covariant: a `String[]` may be viewed as `Object[]`, but a store of the wrong runtime type throws `ArrayStoreException`. Generic `ArrayList<String>` is checked mainly at **compile time**; type parameters are erased at runtime, so there is no array-style store check on `add`.

```java
Object[] cells = new String[1];
try {
    cells[0] = Integer.valueOf(1); // ArrayStoreException
} catch (ArrayStoreException expected) {
    // runtime component type is String
}

List<String> names = new ArrayList<>();
names.add("Ada");
// names.add(1); // compile error with generics
```

**Listing 3.** Arrays enforce component type at store time; a parameterized `ArrayList` rejects bad types at compile time.

## Nesting and APIs

An array type can be multi-dimensional (`int[][]`). One `ArrayList` is a single list level; nest with `List<List<E>>` (or arrays of lists) when you need a grid. Prefer indexed loops or enhanced-`for` for arrays; use `get`/`size`, iterators, or streams for lists. Resize and capacity details: [[How does resize ArrayList]] and [[Does ArrayList always add elements in O(1) time]].

> [!warning] Capacity is not size
> `new ArrayList<>(100)` does **not** create 100 elements. It only reserves capacity; `size()` stays `0` until you `add`. Writing `list.get(0)` before any add throws `IndexOutOfBoundsException`, while `arr[0]` on `new int[100]` is a valid defaulted slot.

> [!warning] “ArrayList cannot be multi-dimensional”
> False as a hard rule. There is no `ArrayList[][]` language type like `int[][]`, but `List<List<Integer>>` (or `ArrayList<ArrayList<Integer>>`) is ordinary nesting.

> [!tip] Interview answer
> **An array has a fixed `length` after creation and can hold primitives or objects. `ArrayList` is a growable `List` over an object array: use `size()`, expect amortized-cost growth on `add`, and box primitives. Prefer a primitive array for fixed numeric buffers; prefer `ArrayList` when the length changes or you need the Collections API.**
