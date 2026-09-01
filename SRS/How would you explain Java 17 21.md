<!--
reps: 0
priority: 0
-->
#Java/Versions/17 #Java/Versions/21 #SRS

# How would you explain Java 17 21

> [!abstract] Short answer
> **Java 17 and 21 are the LTS pair people actually ship, and they are not one feature list.** 17 (GA 14 Sep 2021) finalizes **sealed classes**. Records and `instanceof` patterns were already final in **16**. 21 (GA 19 Sep 2023) finalizes **pattern `switch`**, **virtual threads**, and **sequenced collections**. `StructuredTaskScope` in 21 is a **preview** API, not everyday production.

## Two LTS kits, not one blob

The dump mixes six headlines as if they all arrived together. Split them ([[What is a Java record]], [[How would you explain Sealed classes]], [[How would you explain Virtual Threads]]).

| Feature | Everyday status | What it actually is |
| --- | --- | --- |
| Records | Final in **16** (in 17/21) | Shallowly immutable carrier: canonical constructor, `private final` fields, accessors; implicit `equals` / `hashCode` / `toString` ([[In which Java version were records standardized]], [[What methods does the compiler generate for a Java record]]) |
| `instanceof` type patterns | Final in **16** | `obj instanceof String s` binds without a second cast |
| Sealed types | Final in **17** | `sealed` + `permits` names every direct subtype; foundation for exhaustive patterns |
| Pattern `switch` | **Preview in 17**, final in **21** | `case String s ->`; with a sealed selector the compiler can prove exhaustiveness and skip `default` ([[How do records work with pattern matching in switch]]) |
| Virtual threads | Final in **21** | `Thread` that is not bound 1:1 to an OS thread; cheap thread-per-request for blocking I/O |
| Sequenced collections | Final in **21** (`@since 21`) | `SequencedCollection`: `getFirst` / `getLast` / `addFirst` / `addLast` / `reversed()` |
| Structured concurrency | **Preview in 21** | `StructuredTaskScope` treats forked subtasks as one unit — enable preview, API still moving ([[How would you explain Structured Concurrency]]) |

Sealed subtypes must sit in the same module (named) or the same package (unnamed). Same-file nested types can omit `permits`; the compiler infers them. A permitted type must have a canonical name (no anonymous/local subtypes).

Virtual threads are still `java.lang.Thread`. Create them with `Thread.startVirtualThread(Runnable)` or `Executors.newVirtualThreadPerTaskExecutor()`. They should **not** be pooled. They help I/O-bound concurrency; data-parallel CPU work stays on the Stream API.

`reversed()` is a reverse-ordered **view**. `getFirst` / `getLast` throw `NoSuchElementException` if empty. `addFirst` / `addLast` are optional: the interface default throws `UnsupportedOperationException` (`SortedSet` cannot reposition by fiat). `List` and `Deque` are sequenced; `LinkedHashSet` implements `SequencedSet`.

```d2
direction: down
j16: "16\nrecords, instanceof patterns" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
j17: "17 LTS\nsealed types (switch patterns preview)" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
j21: "21 LTS\npattern switch, virtual threads,\nsequenced collections" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}

j16 -> j17
j17 -> j21
```

**Fig. 1.** Interview trap: records are not “a Java 17 feature.” Pattern `switch` is not final in 17. Structured concurrency is not final in 21.

```java
sealed interface Shape permits Circle, Rect {}
record Circle(double r) implements Shape {}
record Rect(double w, double h) implements Shape {}

class Demo {
    static String label(Object o) {
        return switch (o) { // 21: pattern switch
            case String s -> s;
            case Integer i -> Integer.toString(i);
            default -> "other";
        };
    }

    static int kind(Shape s) {
        return switch (s) { // exhaustive: sealed permits Circle, Rect
            case Circle c -> 1;
            case Rect r -> 2;
        };
    }

    static void endsAndIo() {
        var list = new java.util.ArrayList<>(java.util.List.of("a", "b"));
        list.addFirst("z");
        list.getLast();
        list.reversed();
        Thread.startVirtualThread(() -> {});
    }
}
```

**Listing 1.** Java 21 everyday surface: record + sealed exhaustive `switch`, sequenced ends, `startVirtualThread`. `StructuredTaskScope` is omitted on purpose — it needs preview.

> [!warning] Do not quote the dump’s version blob
> Records and `instanceof` patterns are **16**. Pattern `switch` is **preview in 17**, **final in 21**. Virtual threads and sequenced collections are **21**. `StructuredTaskScope` in 21 is preview (`--enable-preview`); treating it as a stable library is the usual LTS mistake.

> [!warning] Virtual threads are not a faster `ForkJoinPool`
> They are plentiful **threads**, aimed at blocking I/O and thread-per-request. Do not pool them. `synchronized` and some native calls can **pin** a virtual thread to its carrier. `addFirst` on a sequenced **sorted** set throws `UnsupportedOperationException`. Empty `getFirst` throws `NoSuchElementException`, not `null`.

> [!tip] Interview answer
> **17 = LTS with sealed types (records and `instanceof` patterns already landed in 16).** **21 = LTS with virtual threads, sequenced collections, and final pattern `switch`.** Sealed `permits` plus pattern `switch` is what makes exhaustive type switches compile without `default`. Structured concurrency is the preview cousin of virtual threads, not a 21 production API.
