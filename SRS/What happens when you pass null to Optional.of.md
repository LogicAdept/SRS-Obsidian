<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/8 #SRS

# What happens when you pass `null` to `Optional.of`?

> [!abstract] Short answer
> **`Optional.of(null)` throws `NullPointerException` immediately.** `of` only wraps a non-null value. For a possibly-null argument, use `Optional.ofNullable`, which becomes empty instead of throwing.

## Strict factory: non-null or NPE

`public static <T> Optional<T> of(T value)` (Java 8) returns an `Optional` describing that value, which **must** be non-null. If `value` is `null`, it throws `NullPointerException` ([[What is Optional]]).

That is the opposite of `ofNullable`: `ofNullable(null)` is empty; `of(null)` never produces a box that holds `null`. An `Optional` instance does not contain `null` — either you get a present non-null `T`, empty, or this NPE at construction ([[What are Optional.ofNullable and Optional.empty]], [[Why should a method that returns Optional never return null]]).

Use `of` when the value is known to be there (`Optional.of("Ada")`, `Optional.of(user)` after a non-null check). Use `ofNullable` when lifting `Map.get`, a getter, or any API that may return `null`. `Optional.map` follows the `ofNullable` rule for a mapper that returns `null`, so a null mapping becomes empty rather than `of(null)` ([[How does Optional.map work]]).

```d2
direction: down
v: "non-null T" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
n: "null" {
  width: 160
  height: 45
  style.fill: "#fff8e1"
}
of: "Optional.of" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
ofn: "Optional.ofNullable" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
pres: "Optional of T" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
npe: "NullPointerException" {
  width: 220
  height: 45
  style.fill: "#ffebee"
}
empty: "Optional.empty" {
  width: 200
  height: 45
  style.fill: "#fff8e1"
}
v -> of
n -> of
v -> ofn
n -> ofn
of -> pres
of -> npe
ofn -> pres
ofn -> empty
```

**Fig. 1.** `of(null)` is NPE. `ofNullable(null)` is empty. Neither factory stores `null` inside the box.

```java
import java.util.Optional;

class Demo {
    static Optional<String> known() {
        return Optional.of("Ada");
    }

    static Optional<String> ofNull() {
        return Optional.of(null);
    }

    static Optional<String> maybe(String name) {
        return Optional.ofNullable(name);
    }
}
```

**Listing 1.** `known()` is present. Calling `ofNull()` throws `NullPointerException` at `of`, not later at `get`. `maybe(null)` is empty. `maybe("Ada")` and `known()` are both present.

> [!warning] Mixing `of` and `ofNullable` is an NPE at the factory
> `Optional.of(map.get(id))` throws when the key is missing. That NPE looks like “Optional is broken”; it is `of` rejecting `null`. `ofNullable(map.get(id))` is the lift that becomes empty.

> [!warning] You never get `Optional` holding `null`
> A successful `of` is present. Empty is `empty()` / `ofNullable(null)`. There is no third state “present null.” If a method typed as `Optional` returns `null` instead of `empty()`, callers NPE on `of`’s cousins (`map`, `isPresent`) — that is a different bug.

> [!tip] Interview answer
> **`Optional.of(null)` throws `NullPointerException` at once; `of` does not accept null.** Use `of` only for a value you know is non-null. If it might be null, `ofNullable` yields empty instead of throwing.
