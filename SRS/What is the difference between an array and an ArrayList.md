<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Arrays #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **size.** An array is **fixed** after creation. `ArrayList` is **dynamic**; capacity grows when you add elements.

**Performance.** `add` / `get` are described as similar constant-time operations. Automatic resize of `ArrayList` (copy into a new backing array) slows it. A separate dump answers “Array or ArrayList which one is faster?” with **“Array is faster.”** Another dump: for a **fixed-size primitive** list, autoboxing in collections makes them **slower** than a primitive array.

**Primitives.** An array can hold primitives or objects. `ArrayList` holds **objects only**.

**Iterator.** Traverse `ArrayList` with an `Iterator`; arrays with a `for` loop.

**Type safety.** Generics on `ArrayList`. A typed array throws `ArrayStoreException` if you store a wrong runtime type.

**Length.** `ArrayList.size()` vs array `length`.

**Adding.** `ArrayList.add(...)` vs assignment into an array slot.

**Multi-dimension.** An array can be multi-dimensional; an `ArrayList` is always one dimension.

When to use an array over `ArrayList` (dump): size **fixed and known**; primitive arrays avoid wrapper overhead.

```java
int[] arr = new int[2];
arr[0] = 10;
ArrayList<Integer> arrL = new ArrayList<Integer>(2);
arrL.add(30);
```

> [!warning] Unverified traps from the dump
> - “Array is faster” is a one-line dump answer with no operation named.
> - Dump claims `ArrayList` cannot be multi-dimensional (you can still nest lists).
> - Dump treats `add`/`get` as the same cost as a raw array until resize.
