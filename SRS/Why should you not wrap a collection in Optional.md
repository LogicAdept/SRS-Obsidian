<!--
reps: 0
priority: 0
-->
#Java/Language/Optional/Usage #Java/Collections #SRS

# Why should you not wrap a collection in `Optional`?

> [!abstract] Short answer
> **A collection already has “no elements”: `isEmpty()`, size `0`, `Collections.emptyList()` / `emptySet()` / `emptyMap()`.** `Optional<List<T>>` adds a second emptiness (`Optional.empty()` vs a present empty list), so callers unwrap and then iterate. Return the collection; use an empty one when there are no items.

## Zero elements is a collection result, not “no result”

`Optional` is a 0-or-1 box for a method that might have **no result** (`findFirst`, `max`) ([[What is Optional]]). A `List`/`Set`/`Map` already answers “how many?” with `isEmpty()` / `size()`. `Collections.emptyList()` (and `emptySet()`, `emptyMap()`) is the JDK’s immutable empty collection — a real object you can iterate, stream, and return without `null`.

`Optional<List<User>>` therefore has **two** “nothing” states:

- `Optional.empty()` — no list
- `Optional.of(List.of())` / `ofNullable` of an empty list — a list with no users

Callers write `getUsers().orElse(List.of()).forEach(...)` or `ifPresent` then a loop. A plain `List<User>` is one `for` / `.stream()`. An empty list’s stream is empty; you do not need `Optional.stream()` first. If you did wrap the list, `optional.stream()` is a 0-or-1 `Stream<List<User>>`, not a `Stream<User>` ([[How does Optional.stream bridge to the Stream API]]).

Return `results != null ? results : Collections.emptyList()` (or always a list you built). Do not return `null` of the list either; that is the older NPE. Do not return `null` of an `Optional` ([[Why should a method that returns Optional never return null]], [[What are Optional.ofNullable and Optional.empty]]). The same shape applies to arrays (`length == 0`) and maps (`emptyMap()`).

An `Optional<List<T>>` only “makes sense” if a present list is guaranteed non-empty — an odd contract. If “missing query” and “zero rows” are truly different domain events, name them in a type, do not overload Optional-empty vs list-empty.

```d2
direction: down
opt: "Optional<List<User>>" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
a: "Optional.empty()" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
b: "present empty List" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
c: "present non-empty List" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
list: "List<User>" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
empty: "emptyList() — zero users" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
items: "0..n users, iterate" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
opt -> a
opt -> b
opt -> c
list -> empty
list -> items
```

**Fig. 1.** Optional-of-list has two empty channels. A `List` has one: zero or more elements.

```java
import java.util.Collections;
import java.util.List;
import java.util.Optional;

class User {
    final String id;

    User(String id) {
        this.id = id;
    }
}

class Demo {
    private List<User> results;

    Optional<List<User>> getUsersAvoid() {
        return Optional.ofNullable(results);
    }

    List<User> getUsers() {
        return results != null ? results : Collections.emptyList();
    }
}
```

**Listing 1.** `getUsersAvoid()`: `null` results → empty Optional; empty `results` → *present* empty list. `getUsers()` has one empty: `emptyList()`. Do not mutate that immutable empty instance.

> [!warning] Two emptinesses is the interview punchline
> `isPresent()` true and `get().isEmpty()` true is “we have a list with nobody in it.” `isPresent()` false is “we have no list.” Most APIs want one “no users” path. `orElse(emptyList())` papers over the extra state; dropping Optional removes it.

> [!warning] `Optional.stream()` will not flatten the collection
> You get zero or one `List`, then still `flatMap(List::stream)` to reach elements. Returning `List` (or `Stream<User>`) is the direct sequence. Wrapping a collection in Optional is not the same problem as storing Optional *inside* a collection.

> [!tip] Interview answer
> **Do not return `Optional<List<T>>` (or Optional of a Set, Map, or array).** The collection already has empty. Optional adds a second “no items” meaning and an extra unwrap before you can iterate. Return an empty collection, not an empty Optional of a collection.
