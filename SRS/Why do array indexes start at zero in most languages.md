<!--
reps: 0
priority: 0
-->
#Java/Arrays #ProgrammingLanguages #SRS

# Why do array indexes start at zero in most languages

> [!abstract] Short answer
> Because indexing is offset arithmetic: `a[i]` is located at *base address + i × element size*. With zero-based indexing the first element sits exactly at the base address and the index is the raw offset; languages with a separate base bias (index 1 = base + 0) paid an extra subtraction on every access, so C — and Java, which inherited the C model — standardized on 0.

## The offset argument

For a contiguous array the compiler maps `a[i]` to a load at `base + i × elementSize`. Starting at `0` means the index itself is the byte offset measured in elements: no bias term, no wasted address. It also gives clean half-open range arithmetic: the first `n` elements are indexes `0..n-1`, and the count of a range is simply `end - start`. Java keeps this model and adds runtime safety on top: valid indexes are `0..length-1`, and anything outside throws `ArrayIndexOutOfBoundsException` — see [[What is ArrayIndexOutOfBoundsException]].

```java
int[] a = {10, 20, 30, 40};
System.out.println(a[0]);  // 10 — the base address holds the first element
System.out.println(a[3]);  // 40 — last index is length - 1
// a[-1] and a[4] throw ArrayIndexOutOfBoundsException
```

**Listing 1.** Index 0 is the base of the allocation; the largest legal index is `length - 1`.

## The model you can compute

```d2
direction: right
base: "base address\n(element 0)" {
  width: 230
  height: 100
  style.fill: "#e3f2fd"
}
i1: "a[1]\nbase + 1 × 4" {
  width: 200
  height: 100
  style.fill: "#fff3e0"
}
i3: "a[3]\nbase + 3 × 4\nlast element" {
  width: 200
  height: 100
  style.fill: "#e8f5e9"
}
base -> i1: "+4 bytes" {
  style.stroke-dash: 3
}
i1 -> i3: "+2 × 4" {
  style.stroke-dash: 3
}
```

**Fig. 1.** Each step of one element size starts from the base address; index 0 needs no arithmetic at all, which is the whole point of zero-based indexing.

Java is firmly in the zero-based camp: `String.charAt`, `List.get`, and array access all use it, so mixing one-based thinking into loops is a reliable bug generator. The classic off-by-one is a loop condition with `<=` — it walks off the end and throws on the last iteration, because there is no element at index `length`. Keeping every index in `0..length-1` and every range half-open (`start` inclusive, `end` exclusive) removes most of these bugs; see [[What is array in Java]] for the layout details.

> [!warning] Off-by-one is the price of the convention
> Zero-based indexing means the last element is `a[a.length - 1]`. A loop written as `for (int i = 0; i <= a.length; i++)` throws `ArrayIndexOutOfBoundsException` on its final pass — the bounds check happens at run time, not at compile time.

> [!tip] Interview answer
> Index 0 means the index is the offset: element access is just base address plus index times element size, with no bias correction, and ranges become half-open so counts are end minus start. Java inherited this C convention and enforces it with runtime bounds checks — indexes outside `0..length-1` throw.

