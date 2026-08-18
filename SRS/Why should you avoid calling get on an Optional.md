<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Exceptions #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`get()` returns the value if present; on empty it throws `NoSuchElementException`. Calling it without a check swaps NPE for another unchecked exception.

```java
Optional<User> u = find(id);
User user = u.get();  // NoSuchElementException if empty
```

Prefer `orElse`, `orElseGet`, `orElseThrow`, `map`, or `ifPresent`. If absence must fail loudly, dumps prefer `orElseThrow()` over `get()`.

> [!warning] Unverified traps from the dump
> - The exception on empty `get()` is `NoSuchElementException`, not NPE.
