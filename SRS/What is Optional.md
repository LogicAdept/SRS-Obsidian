<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/8 #SRS

# What is `Optional`?

> [!abstract] Short answer
> **`java.util.Optional<T>` (Java 8) is a value-based 0-or-1 container: present non-null `T`, or empty.** It does not store `null`. It is a **method return type** for “no result,” so the signature shows absence instead of a nullable payload. The `Optional` reference itself must not be `null`.

## Present non-null `T`, or empty — never “present null”

The specification: a container object which may or may not contain a **non-null** value. If a value is present, `isPresent()` is `true`; if not, the object is empty and `isPresent()` is `false` ([[What do isPresent and isEmpty do on Optional]]).

Create with `Optional.of(x)` (x must be non-null), `Optional.ofNullable(x)` (null → empty), or `Optional.empty()` ([[What are Optional.ofNullable and Optional.empty]], [[What happens when you pass null to Optional.of]]). Absence is empty, not a null box — return `empty()`, never `null` ([[Why should a method that returns Optional never return null]]).

The API note: primarily a **method return type** where using `null` is likely to cause errors. Callers chain `map` / `flatMap` / `filter` / `ifPresent` / `orElse` instead of `if (value != null)` on the payload ([[How does Optional.map work]], [[When do you use Optional.flatMap instead of map]], [[What does Optional.ifPresent do]]). Java 9 adds `or` (another `Optional`) and `stream()` (a 0-or-1 `Stream`) ([[What does Optional.or do]], [[How does Optional.stream bridge to the Stream API]]).

That does not make `get()` safe. Empty `get()` throws `NoSuchElementException`. Prefer `orElse`, `orElseGet` (lazy `T`), `orElseThrow`, `map`, or `ifPresent`. `isPresent()` then `get()` is still `get()` ([[Why should you avoid calling get on an Optional]], [[What does orElseThrow do on Optional]], [[How would you explain orElse orElseGet]]). A null `Optional` and `of(null)` still throw `NullPointerException`.

It is not a field or parameter type, not `Optional` of a collection, and not `Serializable` ([[Why should you not use Optional as a field or method parameter]], [[Why should you not wrap a collection in Optional]], [[Is Optional serializable]]). Primitive specializations are `OptionalInt` / `OptionalLong` / `OptionalDouble` ([[What are OptionalInt OptionalLong and OptionalDouble]]).

```d2
direction: down
o: "Optional<T>" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
p: "present: non-null T" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
e: "empty: no value" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
bad: "cannot hold null\nof(null) → NPE" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
o -> p
o -> e
o -> bad
```

**Fig. 1.** Two states only. “Contains null” is not one of them.

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
    static Optional<User> find(String id) {
        return "1".equals(id) ? Optional.of(new User("Ada")) : Optional.empty();
    }

    static String label(String id) {
        return find(id).map(User::getName).orElse("unknown");
    }
}
```

**Listing 1.** `find` returns a real `Optional` (empty, not `null`). `label` handles both cases without `isPresent`/`get`. `Optional.of(null)` would throw; `ofNullable` is the lift for a maybe-null payload. Empty `get()` would throw `NoSuchElementException`.

> [!warning] It does not contain `null`
> Dump wording “container that may contain null” is backwards. `of(null)` is `NullPointerException`. `ofNullable(null)` is empty. There is no present-null state.

> [!warning] It does not erase NPE, and it does not force the empty case
> It replaces a nullable *payload* with empty vs present. A null `Optional`, `of(null)`, and empty `get()` still throw. You can still ignore the box. Use combinators and `empty()`; do not treat Optional as a magic null-safe type, and do not answer “it avoids NPE” as the whole story.

> [!tip] Interview answer
> **`Optional` is a Java 8 box: either one non-null value or empty — it never holds null.** Use it as a return type so “no result” is in the signature. Handle it with `map`/`orElse`/`ifPresent`, not `get()`. Do not use it as a field or parameter, and do not wrap a collection.
