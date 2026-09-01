<!--
reps: 0
priority: 0
-->
#Java/Arrays #Java/Streams #Java/Versions/8 #SRS

# Can you turn a Java array into a stream?

> [!abstract] Short answer
> **Yes.** Since Java 8, `Arrays.stream(array)` returns a sequential stream whose source is that array: a `T[]` becomes `Stream<T>`; `int[]` / `long[]` / `double[]` become `IntStream` / `LongStream` / `DoubleStream`. `Stream.of(array)` matches that for **reference** arrays; for a primitive array it does **not**.

## Array as stream source

`Arrays.stream` is the dedicated factory ([[What ways exist to create a Java stream]], [[What is the Java Stream API]]). The whole-array overloads take the array as source. The range overloads take `startInclusive` and `endExclusive` (half-open). A bad range throws `ArrayIndexOutOfBoundsException`: negative start, `endExclusive < startInclusive`, or `endExclusive` past the array length.

The Javadoc states the array is **assumed unmodified** while the stream is in use. The returned stream is sequential; call `parallel()` afterward if you want a parallel pipeline.

There is **no** `Arrays.stream` for `boolean[]`, `byte[]`, `char[]`, `short[]`, or `float[]` — only `T[]`, `int[]`, `long[]`, and `double[]`.

`Stream.of(T... values)` is a varargs factory whose OpenJDK body is `return Arrays.stream(values);`. Passing a `String[]` therefore streams the strings. `Stream.of` also has a single-element overload `of(T t)`. An `int[]` is one object, so `Stream.of(intArray)` is a `Stream<int[]>` of size **1**, not an `IntStream`. Use `Arrays.stream(intArray)` or `IntStream.of(intArray)` (`int...` takes the ints as elements). Same shape for `long[]` / `double[]` with `LongStream` / `DoubleStream`.

`Arrays.asList(array).stream()` is a collection pipeline, not an array factory. For a primitive array, `asList` sees one element (the array object), same family of mistake as `Stream.of(intArray)` ([[What is the difference between Collection and Stream in Java]]).

```d2
direction: down
arr: "array" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
ref: "T[]\nArrays.stream / Stream.of" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
prim: "int[] / long[] / double[]\nArrays.stream → primitive stream" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
trap: "Stream.of(int[])\nStream<int[]> size 1" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
arr -> ref
arr -> prim
arr -> trap
```

**Fig. 1.** Reference arrays: `Arrays.stream` and `Stream.of` agree. Primitive `int`/`long`/`double` arrays need `Arrays.stream` (or `IntStream.of` / …). `Stream.of` on a primitive array boxes the whole array as one element.

```java
import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static Stream<String> refs(String[] names) {
        return Arrays.stream(names);
    }

    static Stream<String> refsViaOf(String[] names) {
        return Stream.of(names);
    }

    static IntStream ints(int[] values) {
        return Arrays.stream(values);
    }

    static IntStream slice(int[] values) {
        return Arrays.stream(values, 1, 3);
    }

    static Stream<int[]> notTheInts(int[] values) {
        return Stream.of(values);
    }

    static IntStream intsViaOf(int[] values) {
        return IntStream.of(values);
    }
}
```

**Listing 1.** `refs` and `refsViaOf` are `Stream<String>`. `ints` and `intsViaOf` are `IntStream`. `notTheInts` is one element: the `int[]` itself. `slice` is indexes `[1, 3)`.

> [!warning] `Stream.of` on a primitive array is a singleton
> `Stream.of(new int[]{1, 2, 3}).count()` is `1`. Summing that stream will not compile as `IntStream.sum`. Use `Arrays.stream` or `IntStream.of`. There is still no `Arrays.stream(char[])` / `byte[]` / `short[]` / `boolean[]` / `float[]` — those types are not primitive-stream sources.

> [!warning] Range indexes are half-open and throw
> `Arrays.stream(a, from, to)` covers `[from, to)`. `to < from`, `from < 0`, or `to > a.length` throws `ArrayIndexOutOfBoundsException`. Mutating the array while a terminal operation runs violates the “unmodified during use” contract.

> [!tip] Interview answer
> **Yes — `Arrays.stream(array)` (Java 8) makes a sequential stream from the array, including a from/to range.** Object arrays can also use `Stream.of(array)`. For `int[]`, `long[]`, and `double[]` you want `Arrays.stream` or `IntStream.of` / `LongStream.of` / `DoubleStream.of`; `Stream.of` on those arrays is a one-element `Stream` of the array object.
