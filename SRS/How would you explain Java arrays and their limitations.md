<!--
reps: 0
priority: 0
-->
#Java/Arrays #SRS

# How would you explain Java arrays and their limitations

> [!abstract] Short answer
> An array is a fixed-length, ordered container of one component type with constant-time indexed access — and its limitations follow from that design: the size never changes, there are no built-in operations beyond `clone`, reference arrays are covariant and throw `ArrayStoreException` at run time, generic array creation is forbidden, and indexes must fit in an `int`.

## The strengths first

An array is one object with a final `length` field and a single component type, which may be a primitive (`int[]`, `long[]`) or a reference type (`String[]`). Access `a[i]` is a bounds-checked offset computation — constant time, cache-friendly, no per-element object header for primitives. The utility class `java.util.Arrays` supplies the standard operations (`sort`, `binarySearch`, `fill`, `copyOf`, `toString`), and streams can wrap arrays for processing — see [[Can you turn a Java array into a stream]]. For the object-vs-primitive classification see [[Is a Java array a primitive or an object]].

## The limitations, one by one

```java
int[] a = new int[3];
List<Integer> dynamic = new ArrayList<>();
dynamic.add(1);
dynamic.add(2);
System.out.println("array length stays " + a.length);
System.out.println("ArrayList grew to " + dynamic.size());

String[] strings = new String[3];
Object[] objects = strings;            // compiles: String[] is an Object[]
objects[0] = "ok";
try {
    objects[1] = Integer.valueOf(42);  // compiles, fails at run time
} catch (ArrayStoreException e) {
    System.out.println("caught " + e);
}
```

**Listing 1.** No append on arrays, and the covariance trap: a wrong element type is a run-time `ArrayStoreException`, not a compile error. Output on JDK 21: `array length stays 3`, `ArrayList grew to 2`, `caught java.lang.ArrayStoreException: java.lang.Integer`.

```d2
direction: right
strings: "String[3]\nreal component type" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
alias: "Object[] alias\n(same object)" {
  width: 200
  height: 100
  style.fill: "#fff3e0"
}
store: "alias[1] = Integer\ncompile ok" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
ase: "runtime store check\nArrayStoreException" {
  width: 260
  height: 100
  style.fill: "#ffebee"
}
strings -> alias: "covariant assignment" {
  style.stroke-dash: 3
}
alias -> store
store -> ase: "JVM checks the real type"
```

**Fig. 1.** The variable type says `Object[]`, the object stays `String[]`; the JVM store check fails and throws `ArrayStoreException`.

The remaining limitations are structural. Size is fixed — growth means reallocating and copying, which is exactly what `ArrayList` automates; see [[What is the difference between an array and an ArrayList]] and [[Is a Java array a static or dynamic data structure]]. Generics do not compose with arrays: `new List<String>[5]` is a compile-time error because the JVM store check needs a reifiable component type. Indexes must be `int` values — a `long` index is a compile-time error, so an array cannot address more than about 2.1 billion elements. And every copy operation is shallow: `clone`, `copyOf`, and `arraycopy` duplicate the top-level slots only.

> [!warning] Covariance is the trap interviewers probe
> `Object[] objects = strings;` compiles because arrays are covariant, but the object is still a `String[]`, so storing an `Integer` throws `ArrayStoreException` at run time. Generics are invariant precisely to move this error to compile time — which is why `List<Object>` cannot alias `List<String>`.

> [!tip] Interview answer
> Arrays give fixed length, one component type, and constant-time checked indexing with `java.util.Arrays` helpers. The limits: no resizing (use `ArrayList`), covariance causes run-time `ArrayStoreException`, generic array creation is forbidden, indexes are `int`-only, and copies are shallow.

