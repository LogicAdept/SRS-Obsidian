<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS

# How does `Optional.map` work?

> [!abstract] Short answer
> **If a value is present, `map` applies the function and returns an `Optional` of the result as if by `ofNullable`; if empty, it returns empty and does not call the function.** A `null` mapping result becomes empty, so the returned box never holds `null`. Use `flatMap` when the function already returns `Optional`.

## Present value in, `Optional` out; empty skips the mapper

`Optional.map` is a Java 8 instance method: `<U> Optional<U> map(Function<? super T, ? extends U> mapper)`. It is the pipeline form of “transform if present”:

- The mapper is required. `Objects.requireNonNull(mapper)` runs **before** the emptiness check, so a `null` function throws `NullPointerException` even on `Optional.empty()`.
- If this `Optional` is empty, `map` returns empty and never calls `mapper.apply`.
- If a value is present, it applies `mapper` to that value and returns `Optional.ofNullable(result)`. A non-null result is a present `Optional<U>`; a `null` result is empty ([[What are Optional.ofNullable and Optional.empty]], [[What happens when you pass null to Optional.of]]).

That `ofNullable` step is why `map` is safe to chain on getters that may return `null`: the next `map`/`filter` sees empty and is skipped. The box itself still never contains `null` ([[What is Optional]]).

`flatMap` is the sibling when the function already returns `Optional`. `map` would wrap that result again (`Optional<Optional<U>>`). `flatMap` does not, and it throws `NullPointerException` if the function returns `null` rather than an `Optional` ([[When do you use Optional.flatMap instead of map]]).

```d2
direction: down
call: "optional.map(mapper)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
npe: "mapper == null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
empty: "empty: skip apply" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
apply: "present: mapper.apply(value)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
ofn: "ofNullable(result)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
outEmpty: "Optional.empty()" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
outVal: "Optional of U" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
call -> npe
call -> empty
call -> apply
empty -> outEmpty
apply -> ofn
ofn -> outVal
ofn -> outEmpty
```

**Fig. 1.** A `null` mapper throws before emptiness is considered. Empty skips `apply`. A present value is wrapped with `ofNullable`, so a `null` result is empty, not `Optional.of(null)`.

```java
import java.util.Optional;

class User {
    private final String name;

    User(String name) {
        this.name = name;
    }

    String getName() {
        return name;
    }
}

class Demo {
    static Optional<String> upperName(Optional<User> user) {
        return user.map(User::getName).map(String::toUpperCase);
    }

    static Optional<String> mapperNullIsEmpty() {
        return Optional.of("present").map(s -> (String) null);
    }

    static Optional<String> emptySkipsMapper() {
        return Optional.<String>empty().map(String::toUpperCase);
    }
}
```

**Listing 1.** `upperName` chains two maps: a `null` name becomes empty, so `toUpperCase` is not called. `mapperNullIsEmpty` is empty because `ofNullable(null)` is empty. `emptySkipsMapper` is empty and does not invoke `toUpperCase`. `Optional.empty().map(null)` still throws `NullPointerException`.

> [!warning] A `null` mapping result is empty, not an `Optional` of `null`
> `map` does **not** call `Optional.of`. `User::getName` returning `null` makes the chain empty; later maps look like they “did nothing.” That is the documented `ofNullable` rule, not a bug. `Optional.of(null)` is a different failure (`NullPointerException` at `of`).

> [!warning] `map` of an `Optional`-returning function nests boxes
> `user.map(u -> findAddress(u))` is `Optional<Optional<Address>>` if `findAddress` already returns `Optional`. Use `flatMap` for that mapper. `flatMap` also differs on `null`: a `null` `Optional` from the mapper is `NullPointerException`, not empty.

> [!tip] Interview answer
> **`map` applies a function to a present value and wraps the result as if by `ofNullable`; empty stays empty and the function is not called.** A `null` result becomes empty, never an `Optional` that holds `null`. Use `flatMap` when the function already returns `Optional`. A `null` mapper throws `NullPointerException` even on an empty `Optional`.
