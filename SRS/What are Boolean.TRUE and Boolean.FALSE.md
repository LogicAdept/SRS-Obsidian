<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list `Boolean.TRUE` as the wrapper example for primitive `true`, alongside `valueOf` / `parseBoolean` / `booleanValue`. `Boolean` is described as caching both boolean values, so identity comparisons of boxed booleans can hit those constants.

Use wrappers when a `boolean` property must also mean unset (`null`).

> [!warning] Unverified traps from the dump
> - Prefer `Boolean.TRUE` / `valueOf` over `new Boolean(true)` in dumps that still show constructors.
