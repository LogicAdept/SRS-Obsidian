<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pre-Java 5 dumps used `public static final int` / String fields (the “enum int / enum String patterns”). Any `int` or `String` could be assigned — no dedicated type, no compiler check (currency `99` with no such coin).

A real `enum` is type-safe: only declared constants are assignable. It has its own namespace, can carry values via a constructor, and works in `switch`.

```java
public enum Currency { PENNY, NICKLE, DIME, QUARTER }
```

> [!warning] Unverified traps from the dump
> - Static imports can shorten int-constant names; dumps still prefer enum for the type.
