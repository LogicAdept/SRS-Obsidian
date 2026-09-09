<!--
reps: 0
priority: 0
-->
#Java/Arrays #SRS

# Is a Java array a static or dynamic data structure

> [!abstract] Short answer
> **Static (fixed-size).** After creation the array object has a final `length` that can never change: there is no append, insert, or remove. To "grow" you build a different array and copy the contents over; the dynamic behavior people expect from arrays is what `ArrayList` implements on top of a backing array.

## What "static" means here

The JLS gives every array a `public final` field `length`; once the object exists, its slot count is frozen. All the flexible operations — grow, shrink, insert in the middle — are missing from the array API. The idiom for growth is explicit reallocation: allocate a bigger array, copy elements (with `Arrays.copyOf` or `System.arraycopy`), and point the variable at the new object. The old object is not modified; it is simply replaced, which is why [[What is the most efficient way to copy an array in Java]] matters for these resizes.

```java
int[] a = {1, 2, 3};
a[3] = 4;                            // ArrayIndexOutOfBoundsException: no growth
int[] bigger = Arrays.copyOf(a, 5);  // new object: [1, 2, 3, 0, 0]
System.out.println(bigger.length);   // 5 — a new array, a is still length 3
```

**Listing 1.** Indexing past the end always throws; `Arrays.copyOf` does not resize `a` — it allocates a second array with the extra slots zero-filled.

## Where the dynamic behavior lives

`ArrayList` keeps a plain `Object[]` inside, tracks a separate logical `size()`, and reallocates a larger backing array when capacity runs out, so callers get amortized constant-time `add`. That is the standard answer to "I want array access with dynamic size" — see [[What is the difference between an array and an ArrayList]]. The fixed-size property is not a defect to work around blindly: fixed length means a stable reference (no reallocation behind your back), no capacity over-allocation, and cheap length checks.

```d2
direction: right
a: "int[3]\nlength 3, final" {
  width: 200
  height: 100
  style.fill: "#e3f2fd"
}
bigger: "int[5]\nnew object\n{1, 2, 3, 0, 0}" {
  width: 220
  height: 110
  style.fill: "#e8f5e9"
}
list: "ArrayList\nsize() 0..capacity\nbacking array reallocated" {
  width: 260
  height: 110
  style.fill: "#fff3e0"
}
a -> bigger: "grow = new array + copy" {
  style.stroke-dash: 3
}
list -> list: "add() handles reallocation for you" {
  style.stroke-dash: 3
}
```

**Fig. 1.** An array can only be replaced, not resized; `ArrayList` automates the same replace-and-copy cycle so the caller never sees it.

> [!warning] `final` freezes the reference, not the contents
> `final int[] xs = {1, 2, 3}` does not make the data constant: `xs[0] = 9` compiles and runs. And calling `xs.length` will never reflect "growth" — any code that claims to enlarge an existing array in place is wrong; it silently replaced the array.

> [!tip] Interview answer
> An array is a static data structure: the `length` field is final and fixed at creation, so elements cannot be appended or removed. Growth is always "allocate a new array and copy" — `ArrayList` is the dynamic wrapper that does exactly that for you behind a resizable API.

