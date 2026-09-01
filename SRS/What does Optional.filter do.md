<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS

# What does `Optional.filter` do?

> [!abstract] Short answer
> **If a value is present and the predicate is true, `filter` returns an `Optional` describing that value; otherwise it returns empty.** An already-empty `Optional` stays empty and the predicate is not called. Present-but-rejected and already-empty are both empty afterward — you cannot tell them apart.

## Keep the value, or drop to empty

`filter` is a Java 8 instance method: `Optional<T> filter(Predicate<? super T> predicate)`. If a value is present **and** `predicate.test(value)` is true, the result describes that same value. If the `Optional` is empty, or the predicate is false, the result is empty ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]], [[What do isPresent and isEmpty do on Optional]]).

The predicate is required: a `null` predicate throws `NullPointerException` even when the `Optional` is empty. When a value is present, a throwing predicate propagates; `filter` does not swallow it.

Unlike `map`, `filter` does not change the type parameter. It is a 0-or-1 keep-or-drop: chain `filter` then `map` to transform only values that passed ([[How does Optional.map work]], [[When do you use Optional.flatMap instead of map]]).

```d2
direction: down
call: "optional.filter(predicate)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
npe: "predicate == null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
empty: "empty: skip test" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
test: "present: predicate.test(value)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
keep: "true → Optional of T" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
drop: "false → empty" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
outEmpty: "empty" {
  width: 200
  height: 45
  style.fill: "#fff8e1"
}
call -> npe
call -> empty
call -> test
empty -> outEmpty
test -> keep
test -> drop
drop -> outEmpty
```

**Fig. 1.** Empty skips the predicate. A failed test and an empty input both finish empty.

```java
import java.util.Optional;

class User {
    private final String name;
    private final int age;
    private final boolean active;

    User(String name, int age, boolean active) {
        this.name = name;
        this.age = age;
        this.active = active;
    }

    String getName() {
        return name;
    }

    int getAge() {
        return age;
    }

    boolean isActive() {
        return active;
    }
}

class Demo {
    static Optional<User> find(String id) {
        return "1".equals(id)
            ? Optional.of(new User("Ada", 36, true))
            : Optional.empty();
    }

    static Optional<User> active(String id) {
        return find(id).filter(User::isActive);
    }

    static String adultName(String id) {
        return find(id)
            .filter(u -> u.getAge() >= 18)
            .map(User::getName)
            .orElse("ineligible");
    }
}
```

**Listing 1.** `active("1")` stays present if `isActive` is true. `adultName` drops under-18 users to empty, then `map` / `orElse`. `find("missing").filter(...)` never calls the predicate. After `filter`, “not found” and “found but rejected” are both empty.

> [!warning] Filtered-out and missing are the same empty
> `isPresent()` cannot tell “predicate was false” from “there was no value.” If you need the reason, branch before `filter` or throw with `orElseThrow` on a pipeline that must not be empty.

> [!warning] `filter` is not `ifPresent`
> The result is still `Optional<T>`. `filter` does not run a side-effect consumer and does not unwrap. A `null` predicate is `NullPointerException`, including on `Optional.empty()`.

> [!tip] Interview answer
> **`filter` keeps a present value only when the predicate is true; otherwise you get empty.** Empty skips the predicate. You cannot tell “missing” from “present but rejected” afterward — both are empty — so chain `map`/`orElse` for the success path.
