<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/8 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Optional.of(value)` wraps a non-null value. If the argument is `null` it throws `NullPointerException` immediately — dumps say that is by design so the mistake shows up at the source.

```java
Optional<String> name = Optional.of("Ada");   // holds "Ada"
Optional<String> bad  = Optional.of(null);    // NullPointerException
```

Use `of` only when the value is known non-null. If it might be `null`, use `ofNullable`.

> [!warning] Unverified traps from the dump
> - Mixing up `of` and `ofNullable` is called a classic NPE where you least expect one.
