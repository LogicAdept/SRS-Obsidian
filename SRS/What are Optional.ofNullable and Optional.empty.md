<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/8 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Optional.ofNullable(value)` wraps a maybe-null value: empty for `null`, present otherwise. `Optional.empty()` is an explicitly empty `Optional`.

```java
Optional<String> a = Optional.ofNullable(maybeNull);
Optional<String> b = Optional.empty();

Optional<User> find(String id) {
    return Optional.ofNullable(map.get(id));
}
```

`ofNullable` is the dump’s bridge from legacy null-returning APIs.

> [!warning] Unverified traps from the dump
> - `of(null)` NPEs; `ofNullable(null)` is empty — that pair is the usual follow-up.
