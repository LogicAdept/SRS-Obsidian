<!--
reps: 0
priority: 0
-->
#Java/Arrays #SRS

# What is array in Java

> [!abstract] Short answer
> An array is a container **object** that stores a fixed number of elements of one component type in contiguous slots, addressed by an `int` index from `0` to `length - 1`. Its `length` is a public final field set at creation, it can hold primitives or references, and every array type descends from `Object`.

## Structure and creation

The component type and the slot count are fixed when the array is created; the slots are zero-initialized (numeric `0`, `false`, or `null` for references). Creation forms: `new int[5]` (five zeroed slots), `{1, 2, 3}` (an array literal — only allowed in a declaration), and `Array.newInstance(String.class, 3)` when the type is known only at run time. A multidimensional array is just an array of array references, so rows can have different lengths. The runtime class of `int[]` is printed as `[I`, `String[]` as `[Ljava.lang.String;` — proof that array types are real classes the JVM knows about.

```java
int[] a = {1, 2, 3};                      // literal: length 3, fixed
int[] fresh = new int[3];                 // slots {0, 0, 0}
String[] strs = new String[2];            // slots {null, null}
System.out.println(a instanceof Object);  // true — every array extends Object
System.out.println(a.length);             // 3 — final field, so last index is 2
System.out.println(int[].class.getName()); // [I
```

**Listing 1.** Arrays are objects with a final `length` field; fresh slots hold default values, not empty strings or zeros you put there.

## Memory model and access

The array variable holds a reference to the array object on the heap. An access `a[i]` is resolved as *base address + i × element size*, which is why indexes start at zero and why reads and writes are constant time — see [[Why do array indexes start at zero in most languages]]. Every access is bounds-checked at run time: an index below `0` or at/above `length` throws `ArrayIndexOutOfBoundsException`. Arrays must be indexed by `int` values (`short`, `byte`, `char` are promoted); a `long` index is a compile-time error.

```d2
direction: right
variable: "int[] a\n(reference variable)" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
object: "array object on the heap\nlength: 3 (final)\nslots [1, 2, 3]\nindexes 0..2" {
  width: 280
  height: 130
  style.fill: "#e8f5e9"
}
variable -> object: "points to" {
  style.stroke-dash: 3
}
```

**Fig. 1.** The variable is only a reference; the object carries the fixed `length` and the slots. Reassigning the variable never changes the object it used to point at.

The `java.util.Arrays` class adds static helpers (`sort`, `binarySearch`, `fill`, `copyOf`, `toString`) — the array object itself has no methods besides `clone` and the members inherited from `Object`, which is why [[Is a Java array a primitive or an object]] is a classic interview question with the answer "an object". For resizable behavior you switch to collections — see [[What is the difference between an array and an ArrayList]].

> [!warning] `length` is a field, and fresh slots are `null`
> Arrays use the field `a.length`, not a `length()` method — `a.length()` does not compile. And `new String[2]` creates two `null` slots, not two empty strings: calling a method on an element before assigning it throws `NullPointerException`.

> [!tip] Interview answer
> An array is a fixed-length container object: one component type, slots addressed by a zero-based `int` index, and a final `length` field. It is itself an object (even `int[]` extends `Object`), access is constant time and bounds-checked, and multidimensional arrays are simply arrays of array references.

