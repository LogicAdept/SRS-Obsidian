<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What is `ArrayIndexOutOfBoundsException`?

> [!abstract] Short answer
> **An unchecked `RuntimeException` thrown when an array is accessed with an illegal index.** The index is negative or greater than or equal to the array's `length`. `int[] a = new int[4]; a[4]` throws: valid indexes are `0` through `3`.

## Illegal index, after a non-null array

`ArrayIndexOutOfBoundsException` extends `IndexOutOfBoundsException`, which extends `RuntimeException`. You do not declare it in `throws` ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]], [[What is the difference between IndexOutOfBoundsException and ArrayIndexOutOfBoundsException]]).

Evaluation order: the array expression runs first, then the index. A `null` array throws `NullPointerException` and never reaches the bounds check. Only then is the index tested: `< 0` or `>= length` throws `ArrayIndexOutOfBoundsException` ([[How do you prevent a NullPointerException]]).

A new `int[4]` has length `4`. The four slots exist; `a[4]` is past the last element, not an “uninitialized” fifth slot. Creating `new int[-1]` is a different type: `NegativeArraySizeException`.

`String.charAt` and `List.get` throw their own `IndexOutOfBoundsException` subtypes (or the parent), not this array type.

```d2
direction: down
access: "a[i]" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
npe: "null array → NullPointerException" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
ok: "0 ≤ i < a.length → component" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
aioob: "i < 0 or i ≥ length → ArrayIndexOutOfBoundsException" {
  width: 400
  height: 50
  style.fill: "#ffebee"
}
access -> npe
access -> ok
access -> aioob
```

**Fig. 1.** Array access: `null` first, then the index range.

```java
class Demo {
    static int lastPlusOne() {
        int[] a = new int[4];
        return a[4];
    }

    static int negative() {
        int[] a = new int[4];
        return a[-1];
    }
}
```

**Listing 1.** `lastPlusOne` and `negative` throw `ArrayIndexOutOfBoundsException` at run time. You may catch it like any unchecked exception ([[Can you catch an unchecked exception in Java]]). Neither method needs `throws` ([[What are common kinds of unchecked exceptions in Java]]).

> [!warning] Length `4` does not make index `4` legal
> Valid indexes are `0 .. length - 1`. Off-by-one at `a[a.length]` is the usual interview snippet.

> [!warning] `null` is `NullPointerException`, not this type
> `int[] a = null; a[0]` throws `NullPointerException`. Bounds are checked only after the reference is non-null.

> [!tip] Interview answer
> **`ArrayIndexOutOfBoundsException` is an unchecked exception for an illegal array index — negative or `>= length`.** `new int[4]; a[4]` throws because indexes run `0` through `3`. A `null` array throws `NullPointerException` instead, and list or string indexes use `IndexOutOfBoundsException`, not this array subclass.
