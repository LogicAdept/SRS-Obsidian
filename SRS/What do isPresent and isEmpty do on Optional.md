<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/11 #SRS

# What do `isPresent` and `isEmpty` do on `Optional`?

> [!abstract] Short answer
> **`isPresent()` is `true` when the box holds a value; `isEmpty()` (Java 11) is `true` when it does not.** They are boolean tests, not unwraps. `isEmpty()` is exactly `!isPresent()`. Prefer `ifPresent`, `map`, `orElse` over `isPresent()` then `get()`.

## Two booleans, one emptiness, different JDK ages

`isPresent()` has been on `Optional` since Java 8: if a value is present, it returns `true`, otherwise `false`. `isEmpty()` arrived in Java 11: if a value is **not** present, it returns `true`, otherwise `false` ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]]).

On a live `Optional` there is no third state. The implementation is the nullness of the inner reference: present iff that reference is non-null. So `o.isPresent() == !o.isEmpty()` always holds. A **`null` `Optional` variable** is outside the type’s contract and throws `NullPointerException` on either call — it is not “empty” ([[What is Optional]], [[Why should a method that returns Optional never return null]]).

Neither method returns the value. `get()` / `orElseThrow()` unwrap and throw `NoSuchElementException` when empty. The documented emptiness checks are `isPresent()` / `isEmpty()`, not `== Optional.empty()` (identity of the empty instance is unspecified).

`if (opt.isPresent()) { opt.get(); }` is the Optional-shaped null check. Prefer `ifPresent` (action if present), `map` / `filter` (stay in the pipeline), or `orElse` / `orElseGet` / `orElseThrow` (unwrap with a defined empty path) ([[What does Optional.ifPresent do]], [[How does Optional.map work]], [[Why should you avoid calling get on an Optional]], [[What does orElseThrow do on Optional]]).

On JDK 8–10 there is no `isEmpty()`: write `!optional.isPresent()`. From 11 on, `isEmpty()` is the readable empty test.

```d2
direction: down
o: "Optional" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
p: "present value" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
e: "empty" {
  width: 220
  height: 45
  style.fill: "#fff8e1"
}
ip: "isPresent() == true\nisEmpty() == false" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ie: "isPresent() == false\nisEmpty() == true" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
o -> p
o -> e
p -> ip
e -> ie
```

**Fig. 1.** `isEmpty()` is Java 11 and the inverse of `isPresent()`. Neither call unwraps.

```java
import java.util.Optional;

class Demo {
    static void dumpStyle(Optional<String> name) {
        if (name.isPresent()) {
            System.out.println(name.get());
        }
        if (name.isEmpty()) {
            System.out.println("not found");
        }
    }

    static String preferred(Optional<String> name) {
        name.ifPresent(System.out::println);
        return name.orElse("not found");
    }

    static boolean inverse(Optional<String> o) {
        return o.isPresent() == !o.isEmpty();
    }
}
```

**Listing 1.** `dumpStyle` is legal and the usual interview smell: `isPresent` + `get`. `preferred` uses `ifPresent` / `orElse`. `inverse` is always `true` for a non-null `Optional` on Java 11+. `isEmpty()` does not compile on Java 8–10.

> [!warning] `isPresent()` then `get()` is still `get()`
> The `if` documents intent; a missed branch still throws `NoSuchElementException`. `ifPresent`, `orElse`, or `orElseThrow` make the empty path obvious. `isEmpty()` does not replace those unwraps.

> [!warning] `isEmpty()` is Java 11
> A Java 8 codebase has only `isPresent()` / `!isPresent()`. `Optional` also has no `isEmpty` overload that takes a predicate — that is `filter`. Do not confuse this with `Collection.isEmpty()` or `String.isEmpty()`; those are different types.

> [!tip] Interview answer
> **`isPresent()` is true when Optional holds a value; `isEmpty()` (Java 11) is the inverse — true when it does not.** They only test; they do not unwrap. Prefer `ifPresent` / `orElse` / `map` instead of `isPresent()` then `get()`, and use `!isPresent()` if you are still on Java 8–10.
