<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A `null` `Optional` reference is the worst of both worlds: the caller writes `result.map(...)` and gets NPE — what Optional was meant to prevent.

```java
Optional<User> find(String id) {
    if (id == null) return null;  // never
}

Optional<User> find(String id) {
    if (id == null) return Optional.empty();
    return Optional.ofNullable(lookup(id));
}
```

The `Optional` reference itself should always be non-null. Absence is `Optional.empty()`.

> [!warning] Unverified traps from the dump
> - Returning `null` instead of empty is a popular lie / code-review trap.
