<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/11 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`isPresent()` is true when a value is held. `isEmpty()` (Java 11+) is the inverse.

```java
if (name.isPresent()) {
    System.out.println(name.get());
}
if (name.isEmpty()) {
    System.out.println("not found");
}
```

Dumps: `isPresent()` then `get()` is null-checking in Optional clothing. Prefer `map`, `ifPresent`, `orElse`.

> [!warning] Unverified traps from the dump
> - `isEmpty` is Java 11+ in this dump; older code only has `!isPresent()`.
