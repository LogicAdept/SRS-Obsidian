<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/9 #SRS

# What does `Optional.or` do?

> [!abstract] Short answer
> **`or(supplier)` (Java 9) returns this `Optional` if a value is present; otherwise it returns the `Optional` the supplier produces.** It does not unwrap: the type stays `Optional<T>`. `orElse` / `orElseGet` return `T`. The supplier runs only when empty.

## Lazy fallback that stays in the box

`or` is `Optional<T> or(Supplier<? extends Optional<? extends T>> supplier)`. If a value is present, it returns an `Optional` describing that value and does not call the supplier. If empty, it returns the `Optional` from `supplier.get()` ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]]).

That is how you chain alternative lookups (`file`, then env, then a default box) and only later unwrap with `orElse` / `orElseGet` / `orElseThrow` ([[What does orElseThrow do on Optional]], [[How would you explain orElse orElseGet]]).

Contrast:

- `orElse(T other)` — unwraps to `T`; `other` is evaluated before the call (eager).
- `orElseGet(Supplier<? extends T>)` — unwraps to `T`; the supplier runs only when empty (lazy `T`).
- `or(Supplier<? extends Optional<? extends T>>)` — lazy **`Optional<T>`**; you can chain `.or(...)`.

A `null` supplier throws `NullPointerException` (the supplier is required even if a value is already present). If the `Optional` is empty and the supplier returns `null` instead of an `Optional`, that is also `NullPointerException` — not empty. Return `Optional.empty()` or `Optional.of(...)` from the supplier ([[Why should a method that returns Optional never return null]]).

```d2
direction: down
call: "optional.or(supplier)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
npeS: "supplier == null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "present: keep this Optional\n(supplier not called)" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
empty: "empty: supplier.get()" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
box: "Optional of T" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
npeR: "supplier returns null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
call -> npeS
call -> ok
call -> empty
empty -> box
empty -> npeR
```

**Fig. 1.** `or` stays in `Optional`. A `null` result from the supplier is NPE, not empty.

```java
import java.util.Optional;

class Config {
    final String name;

    Config(String name) {
        this.name = name;
    }
}

class Demo {
    static final Config DEFAULT = new Config("default");

    static Optional<Config> readFromFile() {
        return Optional.empty();
    }

    static Optional<Config> readFromEnv() {
        return Optional.empty();
    }

    static Optional<Config> cfg() {
        return readFromFile()
            .or(Demo::readFromEnv)
            .or(() -> Optional.of(DEFAULT));
    }

    static Config load() {
        return cfg().orElseThrow();
    }
}
```

**Listing 1.** Each `.or` is skipped once a lookup hits. `Optional.of(DEFAULT)` runs only if file and env were empty. `load` unwraps at the end. `orElseGet(Demo::readFromEnv)` would not compile: `readFromEnv` returns `Optional<Config>`, not `Config`.

> [!warning] `or` is not `orElseGet`
> `orElseGet` yields `T`. `or` yields `Optional<T>`. Passing an `Optional`-returning lookup to `orElseGet` is a type error (or a nested mess if you then `get()`). Passing a `T`-supplier to `or` is a type error.

> [!warning] Supplier `null` means NPE, not empty
> `() -> null` is not `Optional.empty()`. Empty fallback must return an `Optional`. `or` is Java 9; Java 8 has only `orElse` / `orElseGet` / `orElseThrow(supplier)`.

> [!tip] Interview answer
> **`or` (Java 9) is a lazy fallback that still returns `Optional`: present keeps this box, empty uses the supplier’s `Optional`.** That is how you chain lookups without unwrapping. `orElseGet` is the same laziness but returns `T`. A supplier that returns `null` throws `NullPointerException`.
