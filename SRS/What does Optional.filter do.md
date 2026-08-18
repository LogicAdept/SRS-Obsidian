<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`filter(predicate)` keeps the value only if it is present *and* the predicate is true; otherwise empty.

```java
Optional<User> active = find(id).filter(User::isActive);

String name = find(id)
    .filter(u -> u.getAge() >= 18)
    .map(User::getName)
    .orElse("ineligible");
```

An already-empty `Optional` stays empty (predicate not called). Mirrors `Stream.filter` on a 0-or-1 box.

> [!warning] Unverified traps from the dump
> - Empty vs “present but filtered out” look the same afterward — both empty.
