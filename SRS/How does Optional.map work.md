<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`map(function)` transforms the value if present and returns a new `Optional` of the result; if empty, it stays empty and skips the function.

```java
Optional<String> upper = user
    .map(User::getName)
    .map(String::toUpperCase);
```

If the mapper returns `null`, dumps say `map` treats that as empty (`ofNullable` internally) — you never get `Optional` holding `null`. Use `map` for a plain value; `flatMap` when the function returns `Optional`.

> [!warning] Unverified traps from the dump
> - A null mapper result becoming empty is a dump claim to verify against the JDK.
