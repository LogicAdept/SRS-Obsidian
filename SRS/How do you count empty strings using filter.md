<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/String #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you count empty strings using `filter`?

> [!abstract] Short answer
> **`stream.filter(String::isEmpty).count()`.** `filter` keeps elements whose `Predicate` is true; `String.isEmpty()` is true iff `length()` is `0`. `count()` is a terminal reduction and returns `long`.

## Filter, then reduce to a count

A stream pipeline is source → intermediate ops → terminal op. `filter(Predicate)` is intermediate: it returns a stream of matching elements and is lazy until a terminal starts ([[How would you explain what method filter in stream]], [[Which functional interface represents a filter or predicate in the Stream API]], [[When does a Java stream pipeline actually start executing]]). The predicate must be non-interfering and stateless.

`count()` is a terminal reduction, equivalent to `mapToLong(e -> 1L).sum()`. After `filter(String::isEmpty)`, that number is how many strings have length 0 — not how many are blank, and not the source size.

`isEmpty()` (Java 1.6, `CharSequence`) is `length() == 0` only. `" ".isEmpty()` is false. `isBlank()` (Java 11) is empty **or** only whitespace code points — a different question.

```d2
direction: down
src: "Stream<String>" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
fil: "filter(String::isEmpty)\nkeep length 0" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
cnt: "count()\nlong" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
src -> fil
fil -> cnt
```

**Fig. 1.** Intermediate `filter` drops non-empty strings; terminal `count` reduces the rest to a `long`.

```java
import java.util.List;
import java.util.stream.Stream;

class Demo {
    static long emptyCount(List<String> strings) {
        return strings.stream()
            .filter(String::isEmpty)
            .count();
    }

    static long emptyCount(Stream<String> strings) {
        return strings.filter(s -> s != null && s.isEmpty()).count();
    }

    static void demo() {
        emptyCount(List.of("a", "", "  ", "", "b")); // 2
    }
}
```

**Listing 1.** `List.of("a", "", "  ", "", "b")` yields `2`: two `""`, and `"  "` is not empty. The `Stream` overload guards `null` so `String::isEmpty` is not called on `null`.

> [!warning] Empty is not blank, and `null` is not empty
> `String::isEmpty` throws `NullPointerException` on a `null` element. `" ".isEmpty()` is false; use `isBlank()` only if the interviewer asked for whitespace. `""` is the empty string; `new String()` is also empty (`length()` 0).

> [!warning] Bare `count()` can skip the pipeline; `filter` then `count` cannot
> `count()` may skip traversal when the size is known from the source (`list.stream().peek(...).count()` need not print). After `filter`, the result is not the source size, so the predicate **does** run. Do not “optimize” by writing `list.size()` when the question asked to count **empty** strings ([[What terminal stream operations do you know in Java]]).

> [!tip] Interview answer
> **`filter(String::isEmpty)` then `count()` — that is a `long`, and empty means length zero, not whitespace.** Guard `null` if the source can contain it. `isBlank()` is a different Java 11 method.
