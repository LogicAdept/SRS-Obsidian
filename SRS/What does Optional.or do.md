<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/9 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`or(supplier)` (Java 9+) returns this `Optional` if present, otherwise the `Optional` from the supplier. Unlike `orElse` / `orElseGet`, it does **not** unwrap — you stay in `Optional`.

```java
Optional<Config> cfg = readFromFile()
    .or(() -> readFromEnv())
    .or(() -> Optional.of(DEFAULT));
```

The supplier is lazy (called only when empty). Then unwrap with `orElse` / `orElseThrow` at the end.

`orElse` vs `orElseGet` (eager value vs lazy `Supplier` of a value) is a separate vault cue: How would you explain orElse orElseGet.

> [!warning] Unverified traps from the dump
> - `or` vs `orElseGet`: one yields `Optional`, the other unwraps to `T`.
