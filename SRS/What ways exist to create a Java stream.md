<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Versions/8 #SRS

# What ways exist to create a Java stream?

> [!abstract] Short answer
> **From a source, not by `new Stream`.** Usual factories: `Collection.stream()` / `parallelStream()`, `Arrays.stream`, `Stream.of`, `Stream.builder()`, `Stream.iterate` / `generate` (infinite unless bounded), `IntStream.range`, `String.chars()`, `Optional.stream()` (Java 9), `Files.lines` (try-with-resources), plus JDK extras (`Random.ints`, `BufferedReader.lines`, `Pattern.splitAsStream`, `BitSet.stream`, `Stream.concat`). `Map` has no `stream()` — stream the views.

## Package-summary sources, plus the static factories

Package doc lists typical origins: `Collection.stream()` / `parallelStream()`; `Arrays.stream`; static factories (`Stream.of`, `IntStream.range`, `Stream.iterate`); `BufferedReader.lines()`; `Files` path streams; `Random.ints()`; also `BitSet.stream()`, `Pattern.splitAsStream`, `JarFile.stream()` ([[What is the Java Stream API]], [[What is Stream]], [[Can you turn a Java array into a stream]]).

Dump’s eight recipes, checked:

| Recipe | Official note |
| --- | --- |
| Collection `.stream()` | Sequential stream over the collection as of the terminal |
| `Stream.of(...)` | Sequential ordered stream of those values. `Stream.of(int[])` is **one** `int[]`, not `IntStream` — use `Arrays.stream` |
| `Arrays.stream(array)` | Object arrays → `Stream<T>`; `int[]` → `IntStream` |
| `Files.lines(Path)` | `Stream<String>` of **lines**, populated **lazily**. Open file; **close the stream** (try-with-resources). Path overload decodes **UTF-8**. Do not mutate the file during the terminal |
| `"…".chars()` | `IntStream` of zero-extended **`char` values** (surrogates passed through). Not parsed digits |
| `Stream.builder().add(…).build()` | `Stream.Builder` |
| `Stream.iterate(seed, f)` | **Infinite** sequential ordered; pair with `limit` / 3-arg `iterate` (Java 9, `hasNext`) |
| `Stream.generate(supplier)` | **Infinite sequential unordered** |

Also: `Stream.empty()`, `Stream.ofNullable` (9), `Stream.concat(a,b)` (closes both on close), `Optional.stream()` (9), `IntStream.range` / `rangeClosed` ([[How does Optional.stream bridge to the Stream API]], [[What is the Stream limit method for]], [[What is the difference between Collection and Stream in Java]], [[How do you print 10 random numbers using forEach]]).

Collection-backed streams need no `close()`. I/O-backed ones do.

```d2
direction: down
src: "Collection / array / of / iterate\nFiles.lines / chars / Optional" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
st: "Stream / IntStream" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
src -> st
```

**Fig. 1.** A stream always has a source factory. There is no public `Stream` constructor for callers.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static Stream<String> fromList(List<String> words) {
        return words.stream();
    }

    static IntStream digits() {
        return "0123456789".chars(); // char values '0'..'9', not 0..9
    }

    static Stream<String> fileLines(Path path) throws java.io.IOException {
        return Files.lines(path); // caller must close
    }
}
```

**Listing 1.** Collection, `CharSequence.chars()`, and `Files.lines`. Call `fileLines` only inside try-with-resources (or close the returned stream). Infinite `iterate`/`generate` need `limit` (or a short-circuit terminal).

> [!warning] `Stream.of(int[])` is not `IntStream`, and `Files.lines` leaks if you skip `close`
> Primitive arrays: `Arrays.stream`. `Map.stream()` does not exist. `iterate`/`generate` without a bound will not finish. `chars()` is UTF-16 code units as `int`, not `codePoints()` and not `Integer.parseInt`.

> [!tip] Interview answer
> Recite: **`collection.stream()`, `Arrays.stream`, `Stream.of`, `builder`, `iterate`/`generate`, `range`, `String.chars`, `Files.lines` (close it), `Optional.stream`.** Add `concat` and “no `Map.stream()`.” Mention infinite factories need `limit`.
