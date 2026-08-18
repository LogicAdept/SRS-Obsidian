<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The ternary `condition ? a : b` is an expression. A dump trap is type promotion / unboxing of the two branches: if one branch is a primitive and the other a wrapper, the result is unboxed, so a `null` wrapper branch can throw `NullPointerException`.

```java
Integer x = null;
Object o = true ? 0 : x;   // fine
int bad  = false ? 0 : x;  // NPE — both branches unboxed to int
```

> [!warning] Unverified traps from the dump
> - Mixing `int` and `Integer` in a ternary can unbox both branches to `int`.
> - A `null` wrapper then throws `NullPointerException` even on the unused-looking branch that is selected.
