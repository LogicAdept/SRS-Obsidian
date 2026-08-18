<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Streams #Java/Versions/9 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`stream()` (Java 9+) turns an `Optional` into a 0-or-1 `Stream`: empty → empty stream, present → one element. Used to `flatMap` a stream of Optionals and drop empties.

```java
List<User> users = ids.stream()
    .map(this::find)
    .flatMap(Optional::stream)
    .toList();
```

Before Java 9: `.filter(Optional::isPresent).map(Optional::get)`.

> [!warning] Unverified traps from the dump
> - Do not confuse this with wrapping a collection in `Optional` — dumps forbid `Optional<List>`.
