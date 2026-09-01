<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/8 #SRS

# What are `Optional.ofNullable` and `Optional.empty`?

> [!abstract] Short answer
> **`Optional.ofNullable(value)` is the null-tolerant factory: `null` → empty, non-null → present.** **`Optional.empty()` returns an empty `Optional` with no value.** Both exist since Java 8. `Optional.of(value)` is the strict twin: `null` throws `NullPointerException`.

## Two factories for “no value,” and one that rejects `null`

`ofNullable` and `empty` are static methods on `Optional` since 1.8 ([[What is Optional]]):

- `public static <T> Optional<T> ofNullable(T value)` — if `value` is non-`null`, an `Optional` describing that value; if `value` is `null`, an empty `Optional`.
- `public static <T> Optional<T> empty()` — an empty `Optional`. No value is present.

`ofNullable` is how you lift a possibly-null result (`Map.get`, a legacy getter) into the `Optional` pipeline without throwing. `empty()` is the explicit “no result” return when you never had a candidate. Returning `null` from a method whose type is `Optional` is the opposite of this ([[Why should a method that returns Optional never return null]]).

`Optional.of(T value)` requires a non-`null` value and throws `NullPointerException` if you pass `null`. `ofNullable(null)` is empty; `of(null)` is not ([[What happens when you pass null to Optional.of]]). `Optional.map` reuses the `ofNullable` rule for a mapper that returns `null` ([[How does Optional.map work]]).

Do not test emptiness with `==` or `!=` against `Optional.empty()`. The API does **not** guarantee a singleton. Use `isPresent()` (Java 8) or `isEmpty()` (Java 11) ([[What do isPresent and isEmpty do on Optional]]).

```d2
direction: down
n: "null" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
v: "non-null T" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
ofn: "ofNullable" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
of: "of" {
  width: 160
  height: 40
  style.fill: "#ffebee"
}
emp: "empty()" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
empty: "Optional.empty" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
pres: "Optional of T" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
npe: "NullPointerException" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
n -> ofn
v -> ofn
v -> of
n -> of
ofn -> empty
ofn -> pres
of -> pres
of -> npe
emp -> empty
```

**Fig. 1.** `ofNullable` treats `null` as empty. `of` throws. `empty()` is empty with no argument.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

class Demo {
    private final Map<String, String> map = new HashMap<>();

    Optional<String> wrap(String maybeNull) {
        return Optional.ofNullable(maybeNull);
    }

    Optional<String> none() {
        return Optional.empty();
    }

    Optional<String> find(String id) {
        return Optional.ofNullable(map.get(id));
    }

    Optional<String> present() {
        return Optional.of("ok");
    }
}
```

**Listing 1.** `wrap(null)` and `none()` are empty. `find` is the usual lift of `Map.get` (missing key is `null`). `present` uses `of` because the value is known non-null. `Optional.<String>of(null)` throws `NullPointerException` at the call; it does not compile away.

> [!warning] `of(null)` vs `ofNullable(null)`
> Interviews pair these. `of(null)` is `NullPointerException`. `ofNullable(null)` is empty. `ofNullable("x")` and `of("x")` are both present and equal if the values are equal.

> [!warning] `empty() == empty()` is not an emptiness test
> Identity of the empty instance is unspecified. `Optional.empty()` twice may or may not be the same object. `isPresent()` / `isEmpty()` are the documented checks. `ofNullable(null)` is empty by contract, not because it is required to return the same object as `empty()`.

> [!tip] Interview answer
> **`ofNullable` wraps a maybe-null value: null becomes empty, anything else is present.** **`empty()` is the explicit empty box.** Use `of` only when the value cannot be null — `of(null)` throws `NullPointerException`. Never return `null` instead of `empty()`.
