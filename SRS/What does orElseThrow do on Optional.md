<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`orElseThrow(supplier)` returns the value if present, otherwise throws the exception from the supplier. Java 10+ also has no-arg `orElseThrow()` throwing `NoSuchElementException`.

```java
User u = find(id).orElseThrow(() -> new UserNotFoundException(id));
User v = find(id).orElseThrow();
```

Dumps prefer this over `get()`: same failure, reads as intentional, supplier form can throw a domain exception.

> [!warning] Unverified traps from the dump
> - No-arg `orElseThrow()` is Java 10+ in the dump; there is no `#Java/Versions/10` leaf.
