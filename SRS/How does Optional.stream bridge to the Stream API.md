<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Streams #Java/Versions/9 #SRS

# How does `Optional.stream` bridge to the Stream API?

> [!abstract] Short answer
> **`Optional.stream()` (Java 9) is a 0-or-1 sequential `Stream` of the boxed value: empty `Optional` → empty stream, present → a single-element stream.** `Stream.flatMap(Optional::stream)` turns a `Stream<Optional<T>>` into a `Stream<T>` and drops empties, without `isPresent` / `get`.

## A 0-or-1 `Stream`, meant to be `flatMap`ped

`stream()` is an instance method on `Optional` since Java 9: `public Stream<T> stream()`. If a value is present, it returns a **sequential** `Stream` containing only that value; otherwise it returns an empty `Stream` ([[What is Optional]]).

Empty becomes `Stream.empty()`; a present value becomes `Stream.of(value)`. The stream never contains `null`: a present `Optional` already holds a non-null `T`.

The documented bridge is flattening a stream of optionals:

```text
Stream<Optional<T>> os = ...
Stream<T> s = os.flatMap(Optional::stream)
```

`Optional::stream` is a `Function<Optional<T>, Stream<T>>`, which is what `Stream.flatMap` expects. Empties become empty streams and vanish; present values become one-element streams and appear in order. `map(Optional::stream)` is the wrong combinator: that yields `Stream<Stream<T>>`, not `Stream<T>`.

Before `stream()`, the same flattening was `filter(Optional::isPresent).map(Optional::get)`. That is two steps and still uses `get()` ([[What do isPresent and isEmpty do on Optional]], [[Why should you avoid calling get on an Optional]], [[How does Optional.map work]]). `flatMap(Optional::stream)` is the Java 9 replacement.

```d2
direction: down
opt: "Optional<T>" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
st: "optional.stream()" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
empty: "empty Optional\nStream.empty()" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
one: "present\nStream.of(value)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
src: "Stream<Optional<T>>" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
flat: "flatMap(Optional::stream)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
out: "Stream<T>  (empties dropped)" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
opt -> st
st -> empty
st -> one
src -> flat
flat -> out
```

**Fig. 1.** One `Optional` becomes a 0-or-1 sequential stream. A stream of optionals is flattened with `flatMap`, not `map`.

```java
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class Demo {
    static Stream<String> present(Stream<Optional<String>> os) {
        return os.flatMap(Optional::stream);
    }

    static List<String> found(List<String> ids) {
        return ids.stream()
            .map(Demo::find)
            .flatMap(Optional::stream)
            .collect(Collectors.toList());
    }

    static Optional<String> find(String id) {
        return id.isEmpty() ? Optional.empty() : Optional.of(id);
    }
}
```

**Listing 1.** `present` is the JavaDoc recipe: `Stream<Optional<T>>` → `Stream<T>`. `found` maps each id to `Optional`, then keeps only hits. `collect(toList())` is Java 8+; `Stream.toList()` is a later (Java 16) alternative. `stream()` itself is Java 9.

> [!warning] `map(Optional::stream)` nests streams
> `flatMap` concatenates the 0-or-1 streams. `map` leaves you with `Stream<Stream<T>>`. Interviews mix this with `Optional.map` vs `flatMap` ([[When do you use Optional.flatMap instead of map]]).

> [!warning] `stream()` does not flatten a collection inside the box
> If the value is a `List`, `optional.stream()` is a 0-or-1 `Stream<List<…>>` — one list element, not the list’s contents. Use `stream()` on the collection (or `flatMap(Collection::stream)` after you already have a `List`) to iterate elements. That is a different problem than wrapping a collection in `Optional` ([[Why should you not wrap a collection in Optional]]).

> [!tip] Interview answer
> **`Optional.stream()` turns the box into a sequential 0-or-1 `Stream`: empty or a single value.** Bridge a `Stream<Optional<T>>` with `flatMap(Optional::stream)` so empties disappear. That replaces `filter(isPresent).map(get)` and is Java 9; `map` instead of `flatMap` leaves nested streams.
