<!--
reps: 0
priority: 0
-->
#Java/Language/Optional/Usage #SRS

# Why should a method that returns `Optional` never return `null`?

> [!abstract] Short answer
> **A variable of type `Optional` must always refer to an `Optional` instance — never `null`.** Absence is `Optional.empty()` (or `ofNullable` on a missing payload). Returning `null` makes `result.map(...)` / `isPresent()` throw `NullPointerException`, which is the failure `Optional` was meant to replace.

## The box is the null-check; a null box undoes it

`Optional` is documented as a method return type for “no result,” where using `null` is likely to cause errors. The same note says a variable whose type is `Optional` should **never itself be `null`** ([[What is Optional]]).

Callers write `find(id).map(...)`, `filter`, `orElse`, `ifPresent` without a null check on the `Optional` reference. Those are instance methods. If `find` returns `null`, the call is `null.map(...)` and the JVM throws `NullPointerException` before any empty-handling runs ([[How does Optional.map work]], [[What do isPresent and isEmpty do on Optional]]). Empty is a real object: `isPresent()` is `false`, `orElse` supplies a default, `map` is skipped. `null` is not empty.

Return `Optional.empty()` when there is no candidate (`id == null`, not found). Return `Optional.ofNullable(payload)` when the lookup may yield a null payload. Do not return `null` instead of empty, and do not use `of(payload)` if the payload can be null ([[What are Optional.ofNullable and Optional.empty]], [[What happens when you pass null to Optional.of]]). The compiler does not forbid `return null` from an `Optional`-typed method.

```d2
direction: down
m: "Optional<User> find(id)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
n: "return null" {
  width: 220
  height: 45
  style.fill: "#ffebee"
}
e: "return Optional.empty()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
npe: "find(id).map(...)\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "map skipped, orElse works" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
m -> n
m -> e
n -> npe
e -> ok
```

**Fig. 1.** Empty is a usable `Optional`. A null return is a null dereference at the caller.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

class User {
    final String id;

    User(String id) {
        this.id = id;
    }
}

class Demo {
    private final Map<String, User> byId = new HashMap<>();

    Optional<User> findBad(String id) {
        if (id == null) {
            return null;
        }
        return Optional.ofNullable(byId.get(id));
    }

    Optional<User> find(String id) {
        if (id == null) {
            return Optional.empty();
        }
        return Optional.ofNullable(byId.get(id));
    }
}
```

**Listing 1.** `findBad` compiles: `Optional` is a reference type. `findBad(null).isPresent()` throws `NullPointerException`. `find(null).isPresent()` is `false`. Missing keys go through `ofNullable`, not a null `Optional`.

> [!warning] `return null` is a code-review bug the compiler will not catch
> Reviewers look for it because it reintroduces NPE on every combinator. Treat a null `Optional` like a broken invariant, the same as a null that was supposed to be replaced by the type ([[Why should you not use Optional as a field or method parameter]]).

> [!warning] Empty is not `of(null)`
> `Optional.of(null)` throws at the factory. `empty()` / `ofNullable(null)` are the absence values. Returning `null` from the method is a third, illegal state.

> [!tip] Interview answer
> **Never return `null` from a method typed as `Optional` — return `empty()` or `ofNullable`.** Callers assume the reference is a real box and will NPE on `map`/`isPresent` if you lie. Absence lives inside the `Optional`, not in a null reference to the `Optional`.
