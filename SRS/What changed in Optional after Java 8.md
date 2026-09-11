<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What changed in Optional after Java 8

> [!abstract] Short answer
> **Java 9 added `or(Supplier)`, `ifPresentOrElse`, and `stream()`; Java 10 added the zero-arg `orElseThrow()` and deprecated `get()`; Java 11 added `isEmpty()`. Together they closed the main ergonomic gaps that pushed people back to null checks.**

## The three releases, one theme

`or(Supplier<? extends Optional>)` chains alternative optionals lazily — the pre-9 idiom was awkward `map`/`flatMap` gymnastics. `ifPresentOrElse(action, emptyAction)` replaces the `isPresent`/`get` pair in one call. `stream()` turns an `Optional<T>` into a `Stream<T>` of zero or one element, which made `flatMap(Optional::stream)` the standard way to filter absent values inside stream pipelines. `orElseThrow()` with no arguments is `get()` with an honest name — throwing `NoSuchElementException` — and arrived together with `get()`'s deprecation in 10. `isEmpty()` (11) completed the predicate symmetry with `isPresent()`. No new core methods after 11 — later releases changed Optional's neighborhood (records, pattern matching) rather than the class ([[What was new in Java 9 besides modules]] covers the 9 context, [[What was new in Java 11]] the 11 one).

```java
import java.util.Optional;

public class V42_OptionalApi {
    public static void main(String[] args) {
        Optional<String> v = Optional.of("jdk");
        Optional<String> e = Optional.empty();

        v.ifPresentOrElse(x -> System.out.println("present: " + x),
                () -> System.out.println("absent"));                              // 9
        e.ifPresentOrElse(x -> System.out.println(x),
                () -> System.out.println("absent-branch"));                       // 9
        System.out.println("or: " + e.or(() -> Optional.of("fallback")).get());   // 9
        System.out.println("stream count: " + Optional.of("s").stream().count()); // 9
        System.out.println("isEmpty=" + e.isEmpty());                             // 11
        try { e.orElseThrow(); }                                                  // 10
        catch (java.util.NoSuchElementException ex) {
            System.out.println("orElseThrow -> NoSuchElementException");
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V42_OptionalApi in empirics): `present: jdk`, `absent-branch`, `or: fallback`, `stream count: 1`, `isEmpty=true`, `orElseThrow -> NoSuchElementException` (out/V42_OptionalApi.txt).

```d2
direction: right
j9: "Java 9\nor, ifPresentOrElse, stream" { style.fill: "#e8f5e9"; width: 260; height: 70 }
j10: "Java 10\norElseThrow(), get() deprecated" { style.fill: "#e3f2fd"; width: 290; height: 70 }
j11: "Java 11\nisEmpty" { style.fill: "#fff3e0"; width: 160; height: 70 }
j9 -> j10 -> j11: ""
```

**Fig. 1.** Optional's post-8 growth: chaining in 9, naming honesty in 10, symmetry in 11.

> [!warning] `stream()` is the bridge, not a convenience
> Without `Optional.stream()`, pipelines over `List<Optional<T>>` needed `.filter(Optional::isPresent).map(Optional::get)` — exactly the pair that reintroduces the get-smell. `flatMap(Optional::stream)` is the idiom the method was designed for; `orElseThrow()`-without-args and `get()` throw the same exception, so the deprecation is about intent, not behavior.

> [!tip] Interview answer
> **Optional grew in three small steps: Java 9 added lazy or(), terminal ifPresentOrElse, and stream() for pipeline use; Java 10 added the honest orElseThrow() alias and deprecated get(); Java 11 added isEmpty(). Since then the class itself is stable — the API is complete, and newer work went into surrounding language features.**
