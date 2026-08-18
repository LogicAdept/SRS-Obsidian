<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A collection already has empty. `Optional<List<User>>` makes the caller unwrap and then iterate, with two “no items” meanings (empty Optional vs empty list).

```java
Optional<List<User>> getUsers();  // anti-pattern

List<User> getUsers() {
    return results != null ? results : Collections.emptyList();
}
```

Never return `Optional` of a collection, array, or map — return empty instead.

> [!warning] Unverified traps from the dump
> - Two emptiness states is the interview punchline.
