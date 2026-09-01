<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Exceptions/Unchecked #SRS

# What is wrong with `null` and how do you avoid it?

> [!abstract] Short answer
> **`null` is a reference that is not an object: using it as one throws `NullPointerException`.** It also collapses different meanings (missing vs “mapped to null”). Avoid it at API boundaries: return `Optional` for a maybe-value, return an empty collection instead of a null list, and `Objects.requireNonNull` arguments that must exist.

## `null` is not an object, and it is a poor “no result”

`NullPointerException` is thrown when the program uses `null` where an object is required: instance method, field, array length/slot, or `throw null` ([[What is NullPointerException]], [[How do you prevent a NullPointerException]]). That crash is late — the type system still type-checks `User u = null`.

`null` is also ambiguous. `Map.get(key)` returns `null` if the key is absent **or** if the key maps to `null`; you need `containsKey` to tell them apart. One token, two facts.

Java 8 `Optional` exists as a method **return type** where using `null` for “no result” is likely to cause those errors ([[What is Optional]]). Empty vs present is in the type. Lift a maybe-null payload with `ofNullable` (`Map.get`, a getter). Never return a null `Optional`; never `of(null)` ([[What are Optional.ofNullable and Optional.empty]], [[What happens when you pass null to Optional.of]], [[Why should a method that returns Optional never return null]]). Handle the box with `map` / `orElse` / `ifPresent`, not `get()` ([[Why should you avoid calling get on an Optional]]).

That is not “replace every `null` with Optional.” Required constructor/method arguments: `Objects.requireNonNull(x)` (fail at the boundary with NPE). Zero items: `Collections.emptyList()`, not `null` and not `Optional<List>` ([[Why should you not wrap a collection in Optional]]). Do not store Optional in fields or take it as a parameter ([[Why should you not use Optional as a field or method parameter]]).

```d2
direction: down
n: "null used as object" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
npe: "NullPointerException" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
opt: "return Optional\n(no result)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
col: "return emptyList()\n(no elements)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
req: "requireNonNull\n(required arg)" {
  width: 240
  height: 70
  style.fill: "#fff8e1"
}
n -> npe
req -> npe
```

**Fig. 1.** Dereferencing `null` is NPE. APIs should not use `null` to mean “no result” or “no elements.” `requireNonNull` still throws — on purpose — when a required value is missing.

```java
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

class User {
    final String name;

    User(String name) {
        this.name = Objects.requireNonNull(name, "name");
    }
}

class Demo {
    static Optional<User> find(Map<String, User> byId, String id) {
        return Optional.ofNullable(byId.get(id));
    }

    static List<User> listOrEmpty(List<User> found) {
        return found != null ? found : Collections.emptyList();
    }

    static String label(Optional<User> u) {
        return u.map(x -> x.name).orElse("unknown");
    }
}
```

**Listing 1.** `find` makes “no mapping” empty Optional (`ofNullable` cannot tell a null value from a missing key — same `null` from `get`). `listOrEmpty` has one empty. `User` rejects a null name at construction. `label` does not call `get()`.

> [!warning] Optional is not a null-proof type
> `of(null)` is NPE. A null `Optional` NPEs on `map`. Empty `get()` is `NoSuchElementException`. Combinators and `empty()` are the point; sprinkling Optional on fields does not “avoid null.”

> [!warning] `ofNullable(map.get(k))` erases Map’s two nulls
> Missing key and null value both become empty. If those must differ, `containsKey` (or a type that is not `null`) — Optional does not restore the distinction.

> [!tip] Interview answer
> **`null` is not an object, so using it throws `NullPointerException`, and it often means two things at once (absent vs stored null).** Return `Optional` for a maybe-value, an empty collection for no elements, and `requireNonNull` for arguments that must be there. Do not return a null `Optional` or wrap a `List` in Optional.
