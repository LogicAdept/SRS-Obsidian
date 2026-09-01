<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS

# When do you use `Optional.flatMap` instead of `map`?

> [!abstract] Short answer
> **Use `flatMap` when the function already returns `Optional`.** `map` would wrap that result again (`Optional<Optional<T>>`). `flatMap` applies the function and does not add a second box. Use `map` when the function returns a plain `T` (including `null`, which becomes empty).

## One box in, one box out — or two

`map` and `flatMap` are both Java 8 instance methods. If the `Optional` is empty, both skip the function and return empty ([[How does Optional.map work]], [[What is Optional]]).

If a value is present:

- `map(Function<? super T, ? extends U>)` applies the function and wraps the result **as if by `ofNullable`**. A non-null `U` becomes `Optional<U>`; a `null` `U` becomes empty. If `U` is itself `Optional<V>`, the type is `Optional<Optional<V>>`.
- `flatMap(Function<? super T, ? extends Optional<? extends U>>)` applies an **`Optional`-bearing** function and returns that `Optional` as-is — “does not wrap it within an additional `Optional`.”

So: getter returns `Address` → `map(User::getAddress)` is `Optional<Address>`. Getter returns `Optional<Address>` → `flatMap(User::getAddress)` is `Optional<Address>`; `map` is the nested type.

A `null` mapper function is `NullPointerException` for both. A `null` *result* differs: `map` treats it as empty; `flatMap` throws `NullPointerException` if the function returns `null` instead of an `Optional`. Return `Optional.empty()`, never `null`, from a method typed as `Optional` ([[Why should a method that returns Optional never return null]], [[What are Optional.ofNullable and Optional.empty]]).

Chain `flatMap` for each Optional-returning step, then `map` for a plain property (`getZip()` → `String`), then `orElse` to unwrap.

```d2
direction: down
u: "Optional<User>" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
map: "map(User::getAddress)\ngetAddress → Optional<Address>" {
  width: 340
  height: 70
  style.fill: "#ffebee"
}
nested: "Optional<Optional<Address>>" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
fm: "flatMap(User::getAddress)" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
one: "Optional<Address>" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
u -> map
map -> nested
u -> fm
fm -> one
```

**Fig. 1.** `map` adds a layer around an `Optional` result. `flatMap` does not.

```java
import java.util.Optional;

class Address {
    private final String zip;

    Address(String zip) {
        this.zip = zip;
    }

    String getZip() {
        return zip;
    }
}

class User {
    private final Optional<Address> address;

    User(Optional<Address> address) {
        this.address = address;
    }

    Optional<Address> getAddress() {
        return address;
    }
}

class Demo {
    static Optional<User> find(String id) {
        return "1".equals(id)
            ? Optional.of(new User(Optional.of(new Address("02139"))))
            : Optional.empty();
    }

    static Optional<Optional<Address>> nested(String id) {
        return find(id).map(User::getAddress);
    }

    static Optional<Address> address(String id) {
        return find(id).flatMap(User::getAddress);
    }

    static String zip(String id) {
        return find(id)
            .flatMap(User::getAddress)
            .map(Address::getZip)
            .orElse("unknown");
    }
}
```

**Listing 1.** `nested` is what `map` actually types to — it does not compile as `Optional<Address>`. `address` is one layer. `zip` uses `flatMap` then `map` because `getZip` returns `String`, not `Optional<String>`. `User::getAddress` returning `null` (not `empty()`) makes `flatMap` throw.

> [!warning] `map` of an Optional-returning method is the nested-wrapper bug
> Interviewers assign `Optional<Address> a = user.map(User::getAddress)` and wait for the compile error (or a later `.get().get()`). If `getAddress` already returns `Optional`, the combinator is `flatMap`.

> [!warning] `flatMap` does not turn `null` into empty
> `map` uses `ofNullable` on the function result. `flatMap` requires a real `Optional`; `null` is `NullPointerException`. That is the same rule as `or`’s supplier ([[What does Optional.or do]]).

> [!tip] Interview answer
> **Use `flatMap` when the mapper already returns `Optional`, so you do not get `Optional<Optional<T>>`.** Use `map` when it returns a plain value; a null result there becomes empty. `flatMap` throwing on a null `Optional` means the function must return `empty()`, not `null`.
